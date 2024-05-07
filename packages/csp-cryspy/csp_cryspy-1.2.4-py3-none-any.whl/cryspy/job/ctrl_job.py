'''
Control jobs
'''

import itertools
from logging import getLogger
import os
import shutil
import subprocess

import numpy as np

from ..interface import select_code
from ..IO import read_input as rin
from ..IO import change_input, io_stat, pkl_data
from ..IO.out_results import out_rslt, out_hdist
from ..util.utility import backup_cryspy
from ..util.struc_util import out_poscar, out_cif

if rin.algo == 'BO':
    from ..BO.select_descriptor import select_descriptor
    from ..BO import bo_next_select
if rin.algo in ['EA', 'EA-vc']:
    from ..EA import ea_next_gen
if rin.algo == 'EA-vc':
    from ..EA.calc_ef import calc_ef
    from ..EA.calc_hull import calc_convex_hull_2d
if rin.algo == 'LAQA':
    from ..LAQA.calc_score import calc_laqa_bias
    from ..LAQA import laqa_next_selection
    from ..IO.out_results import out_laqa_status, out_laqa_step, out_laqa_score
    from ..IO.out_results import out_laqa_energy, out_laqa_bias


logger = getLogger('cryspy')

class Ctrl_job:

    def __init__(self, stat, init_struc_data):
        self.stat = stat
        self.init_struc_data = init_struc_data
        self.opt_struc_data = pkl_data.load_opt_struc()
        self.rslt_data = pkl_data.load_rslt()
        self.recheck = False
        self.logic_next = False
        # ---------- for each algorithm
        if rin.algo == 'RS':
            self.id_queueing, self.id_running = pkl_data.load_rs_id()
        elif rin.algo == 'BO':
            (self.n_selection, self.id_queueing,
             self.id_running, self.id_select_hist) = pkl_data.load_bo_id()
            (self.init_dscrpt_data, self.opt_dscrpt_data,
             self.bo_mean, self.bo_var, self.bo_score) = pkl_data.load_bo_data()
            (self.init_dscrpt_data, self.opt_dscrpt_data,
             self.bo_mean, self.bo_var,
             self.bo_score) = pkl_data.load_bo_data()
        elif rin.algo == 'LAQA':
            (self.id_queueing, self.id_running,
             self.id_select_hist) = pkl_data.load_laqa_id()
            (self.tot_step_select, self.laqa_step,
             self.laqa_struc, self.laqa_energy,
             self.laqa_bias, self.laqa_score) = pkl_data.load_laqa_data()
        elif rin.algo in ['EA', 'EA-vc']:
            (self.gen, self.id_queueing,
             self.id_running) = pkl_data.load_ea_id()
            if rin.struc_mode in ['mol', 'mol_bs']:
                self.struc_mol_id = pkl_data.load_struc_mol_id()
            if rin.algo == 'EA-vc':
                self.nat_data, self.ratio_data, self.hdist_data = pkl_data.load_ea_vc_data()
            # do not have to load ea_data here.
            # ea_data is used only in ea_next_gen.py
        # ---------- for option
        if rin.kpt_flag:
            self.kpt_data = pkl_data.load_kpt()
        if rin.energy_step_flag:
            self.energy_step_data = pkl_data.load_energy_step()
        if rin.struc_step_flag:
            self.struc_step_data = pkl_data.load_struc_step()
        if rin.force_step_flag:
            self.force_step_data = pkl_data.load_force_step()
        if rin.stress_step_flag:
            self.stress_step_data = pkl_data.load_stress_step()
        # ---------- flag for next selection or generation
        if rin.algo in ['BO', 'LAQA', 'EA', 'EA-vc']:
            if (self.id_queueing or self.id_running):
                self.go_next_sg = False
            else:
                self.go_next_sg = True

    def check_job(self):
        # ---------- option: recalc
        if rin.recalc:
            self.set_recalc()
        # ---------- temporarily append
        self.tmp_running = self.id_running[:]    # shallow copy
        self.tmp_queueing = self.id_queueing[:]
        if not rin.stop_next_struc:    # if true --> option: stop_next_struc
            while len(self.tmp_running) < rin.njob and self.tmp_queueing:
                self.tmp_running.append(self.tmp_queueing.pop(0))
        # ---------- initialize
        self.stage_stat = {}    # key: Structure ID
        self.job_stat = {}
        # ---------- check job status
        for cid in self.tmp_running[:rin.njob]:
            # ------ mkdir
            if not os.path.isdir(f'work/{cid:06}'):
                os.mkdir(f'work/{cid:06}')
            # ------ check stat_job file
            stat_path = f'work/{cid:06}' + '/stat_job'
            try:
                with open(stat_path, 'r') as fstat:
                    istat = fstat.readline()    # id
                    sstat = fstat.readline()    # stage
                    jstat = fstat.readline()    # submitted or done or ...
                self.stage_stat[cid] = int(sstat.split()[0])
                if not cid == int(istat.split()[0]):
                    logger.error(f'ID is wrong in work/{cid:06}')
                    raise SystemExit(1)
                self.stage_stat[cid] = int(sstat.split()[0])
                if jstat[0:3] == 'sub':
                    self.job_stat[cid] = 'submitted'
                elif jstat[0:4] == 'done':
                    self.job_stat[cid] = 'done'
                elif jstat[0:4] == 'skip':
                    self.job_stat[cid] = 'skip'
                else:
                    self.job_stat[cid] = 'else'
            except IOError:
                self.stage_stat[cid] = 'no_file'
                self.job_stat[cid] = 'no_file'

    def set_recalc(self):
        # ---------- check id
        for tid in rin.recalc:
            if tid not in self.opt_struc_data:
                logger.error(f'ID {tid} has not yet been calculated')
                raise SystemExit(1)
        # ---------- append IDs to the head of id_queueing
        self.id_queueing = rin.recalc + self.id_queueing
        io_stat.set_id(self.stat, 'id_queueing', self.id_queueing)
        self.save_id_data()
        # ---------- log and out
        logger.info('# -- Recalc')
        logger.info(f'Append {rin.recalc} to the head of id_queueing')
        # ---------- clear recalc
        rin.recalc = []
        config = change_input.config_read()
        change_input.change_option(config, 'recalc', '')    # clear
        change_input.write_config(config)
        logger.info('Clear recalc in cryspy.in')
        io_stat.set_input_common(self.stat, 'option', 'recalc', '')
        io_stat.write_stat(self.stat)

    def handle_job(self):
        logger.info('# ---------- job status')
        for cid in self.tmp_running[:rin.njob]:
            # ---------- set work_path and cid
            self.work_path = f'./work/{cid:06}/'
            self.cid = cid
            # ---------- handle job
            if self.job_stat[cid] == 'submitted':
                logger.info(f'ID {cid:>6}: still queueing or running')
            elif self.job_stat[cid] == 'done':
                self.ctrl_done()
            elif self.job_stat[cid] == 'skip':
                self.ctrl_skip()
            elif self.job_stat[cid] == 'else':
                logger.error(f'Wrong job_stat in {self.work_path}. ')
            elif self.job_stat[cid] == 'no_file':
                self.ctrl_next_struc()
            else:
                logger.error(f'Unexpected error in {self.work_path}stat_job')

    def ctrl_done(self):
        self.cstage = self.stage_stat[self.cid]
        # ---------- log
        logger.info(f'ID {self.cid:>6}: Stage {self.cstage} Done!')
        # ---------- next stage
        if self.cstage < rin.nstage:
            self.ctrl_next_stage()
        # ---------- collect result
        elif self.cstage == rin.nstage:
            self.ctrl_collect()
        # ---------- error
        else:
            logger.error('Wrong stage in '+self.work_path+'stat_job')
            raise SystemExit(1)

    def ctrl_next_stage(self):
        # ---------- EA-vc
        if rin.algo == 'EA-vc':
            nat = self.nat_data[self.cid]
        else:
            nat = rin.nat
        # ---------- energy step
        if rin.energy_step_flag:
            self.energy_step_data = select_code.get_energy_step(
                self.energy_step_data, self.cid, self.work_path, nat)
        # ---------- struc step
        if rin.struc_step_flag:
            self.struc_step_data = select_code.get_struc_step(
                self.struc_step_data, self.cid, self.work_path, nat)
        # ---------- force step
        if rin.force_step_flag:
            self.force_step_data = select_code.get_force_step(
                self.force_step_data, self.cid, self.work_path, nat)
        # ---------- stress step
        if rin.stress_step_flag:
            self.stress_step_data = select_code.get_stress_step(
                self.stress_step_data, self.cid, self.work_path)
        # ---------- next stage
        if rin.kpt_flag:
            skip_flag, self.kpt_data = select_code.next_stage(
                self.cstage, self.work_path, nat,
                kpt_data=self.kpt_data, cid=self.cid)
        else:
            skip_flag = select_code.next_stage(self.cstage,
                                               self.work_path, nat)
        # ---------- skip
        if skip_flag:
            self.ctrl_skip()
            return
        # ---------- prepare jobfile
        self.prepare_jobfile()
        # ---------- submit
        self.submit_next_stage()

    def submit_next_stage(self):
        # ---------- submit job
        os.chdir(self.work_path)    # cd work_path
        with open('stat_job', 'w') as fwstat:
            fwstat.write(f'{self.cid:<6}    # Structure ID\n')
            fwstat.write(f'{self.cstage + 1:<6}    # Stage\n')
            fwstat.write('submitted\n')
        with open('sublog', 'w') as logf:
            subprocess.Popen([rin.jobcmd, rin.jobfile],
                             stdout=logf, stderr=logf)
        os.chdir('../../')    # go back to ..
        # ---------- save status
        io_stat.set_stage(self.stat, self.cid, self.cstage + 1)
        io_stat.write_stat(self.stat)
        # ---------- log
        logger.info(f'    submitted job, ID {self.cid:>6} Stage {self.cstage + 1}')

    def ctrl_collect(self):
        # ---------- EA-vc
        if rin.algo == 'EA-vc':
            nat = self.nat_data[self.cid]
        else:
            nat = rin.nat
        # ---------- energy step
        if rin.energy_step_flag:
            self.energy_step_data = select_code.get_energy_step(
                self.energy_step_data, self.cid, self.work_path, nat)
        # ---------- struc step
        if rin.struc_step_flag:
            self.struc_step_data = select_code.get_struc_step(
                self.struc_step_data, self.cid, self.work_path, nat)
        # ---------- force step
        if rin.force_step_flag:
            self.force_step_data = select_code.get_force_step(
                self.force_step_data, self.cid, self.work_path, nat)
        # ---------- stress step
        if rin.stress_step_flag:
            self.stress_step_data = select_code.get_stress_step(
                self.stress_step_data, self.cid, self.work_path)
        # ---------- each algo
        if rin.algo == 'RS':
            self.ctrl_collect_rs(nat)
        elif rin.algo == 'BO':
            self.ctrl_collect_bo(nat)
        elif rin.algo == 'LAQA':
            self.ctrl_collect_laqa(nat)
        elif rin.algo in ['EA', 'EA-vc']:
            self.ctrl_collect_ea(nat)
        else:
            logger.error('Error, algo')
            raise SystemExit(1)
        # ---------- move to fin
        if rin.algo == 'LAQA':
            if self.fin_laqa:
                self.mv_fin()
            else:
                os.rename(self.work_path+'stat_job',
                          self.work_path+'prev_stat_job')
        else:
            self.mv_fin()
        # ---------- update status
        self.update_status(operation='fin')
        # ---------- recheck
        self.recheck = True

    def ctrl_collect_rs(self, nat):
        # ---------- get opt data
        opt_struc, energy, magmom, check_opt = \
            select_code.collect(self.cid, self.work_path, nat)
        logger.info(f'    collect results: E = {energy} eV/atom')
        # ---------- register opt_struc
        spg_sym, spg_num, spg_sym_opt, spg_num_opt = self.regist_opt(opt_struc)
        # ---------- save rslt
        self.rslt_data.loc[self.cid] = [spg_num, spg_sym,
                                               spg_num_opt, spg_sym_opt,
                                               energy, magmom, check_opt]
        pkl_data.save_rslt(self.rslt_data)
        out_rslt(self.rslt_data)

    def ctrl_collect_bo(self, nat):
        # ---------- get opt data
        opt_struc, energy, magmom, check_opt = \
            select_code.collect(self.cid, self.work_path, nat)
        logger.info(f'    collect results: E = {energy} eV/atom')
        # ---------- register opt_struc
        spg_sym, spg_num, spg_sym_opt, spg_num_opt = self.regist_opt(opt_struc)
        # ---------- save rslt
        self.rslt_data.loc[self.cid] = [self.n_selection,
                                               spg_num, spg_sym,
                                               spg_num_opt, spg_sym_opt,
                                               energy, magmom, check_opt]
        pkl_data.save_rslt(self.rslt_data)
        out_rslt(self.rslt_data)
        # ---------- success
        if opt_struc is not None:
            # ------ calc descriptor for opt sturcture
            tmp_dscrpt = select_descriptor({self.cid: opt_struc})
            # ------ update descriptors
            self.opt_dscrpt_data.update(tmp_dscrpt)
        # ---------- error
        else:
            # ------ update descriptors and non_error_id
            self.opt_dscrpt_data[self.cid] = None
        # ---------- save bo_data
        self.save_data()

    def ctrl_collect_laqa(self, nat):
        # ---------- flag for finish
        self.fin_laqa = False
        # ---------- get opt data
        opt_struc, energy, magmom, check_opt = \
            select_code.collect(self.cid, self.work_path, nat)
        # ---------- total step and laqa_step
        #     force_step_data[ID][stage][step][atom]
        if self.force_step_data[self.cid][-1] is None:
            self.laqa_step[self.cid].append(0)
        else:
            self.tot_step_select[-1] += len(
                self.force_step_data[self.cid][-1])
            self.laqa_step[self.cid].append(
                len(self.force_step_data[self.cid][-1]))
        # ------ save status
        io_stat.set_common(self.stat, 'total_step', sum(self.tot_step_select))
        io_stat.write_stat(self.stat)
        # ---------- append laqa struc
        self.laqa_struc[self.cid].append(opt_struc)
        # ---------- append laqa energy
        self.laqa_energy[self.cid].append(energy)
        # ---------- append laqa bias
        #     force_step_data[ID][stage][step][atom]
        #     stress_step_data[ID][stage][step][atom]
        tmp_laqa_bias = calc_laqa_bias(
            self.force_step_data[self.cid][-1],
            self.stress_step_data[self.cid][-1],
            wf=rin.wf, ws=rin.ws)
        self.laqa_bias[self.cid].append(tmp_laqa_bias)
        # ---------- append laqa score
        if check_opt == 'done' or np.isnan(energy) or np.isnan(tmp_laqa_bias):
            self.laqa_score[self.cid].append(-float('inf'))
        else:
            self.laqa_score[self.cid].append(-energy + tmp_laqa_bias)
        # ---------- save and out laqa data
        self.save_data()
        out_laqa_status(self.laqa_step, self.laqa_score,
                        self.laqa_energy, self.laqa_bias)
        out_laqa_step(self.laqa_step)
        out_laqa_score(self.laqa_score)
        out_laqa_energy(self.laqa_energy)
        out_laqa_bias(self.laqa_bias)
        # ---------- case of 'done' or error
        if check_opt == 'done' or np.isnan(energy) or np.isnan(tmp_laqa_bias):
            self.fin_laqa = True
            logger.info(f'    collect results: E = {energy} eV/atom')
            # ------ register opt_struc
            (spg_sym, spg_num,
             spg_sym_opt, spg_num_opt) = self.regist_opt(opt_struc)
            # ------ save rslt
            self.rslt_data.loc[self.cid] = [spg_num, spg_sym,
                                                   spg_num_opt, spg_sym_opt,
                                                   energy, magmom, check_opt]
            pkl_data.save_rslt(self.rslt_data)
            out_rslt(self.rslt_data)

    def ctrl_collect_ea(self, nat):
        # ---------- get opt data
        opt_struc, energy, magmom, check_opt = \
            select_code.collect(self.cid, self.work_path, nat)
        logger.info(f'    collect results: E = {energy} eV/atom')
        # ---------- calculate Ef
        if rin.algo == 'EA-vc':
            ef = calc_ef(energy, self.ratio_data[self.cid], rin.end_point)
            logger.info(f'                     Ef = {ef} eV/atom')
        # ---------- register opt_struc
        spg_sym, spg_num, spg_sym_opt, spg_num_opt = self.regist_opt(opt_struc)
        # ---------- save rslt
        if not rin.algo == 'EA-vc':
            self.rslt_data.loc[self.cid] = [self.gen,
                                            spg_num, spg_sym,
                                            spg_num_opt, spg_sym_opt,
                                            energy, magmom, check_opt]
        else:
            self.rslt_data.loc[self.cid] = [self.gen,
                                            spg_num, spg_sym,
                                            spg_num_opt, spg_sym_opt,
                                            energy, ef, magmom, check_opt]
        pkl_data.save_rslt(self.rslt_data)
        if rin.algo == 'EA':
            out_rslt(self.rslt_data)
        if rin.algo == 'EA-vc':
            out_rslt(self.rslt_data, order_ef=True)

    def regist_opt(self, opt_struc):
        '''
        Common part in ctrl_collect_*
        '''
        # ---------- get initial spg info
        try:
            spg_sym, spg_num = self.init_struc_data[
                self.cid].get_space_group_info(symprec=rin.symprec)
        except TypeError:
            spg_num = 0
            spg_sym = None
        # ---------- success
        if opt_struc is not None:
            # ------ get opt spg info
            try:
                spg_sym_opt, spg_num_opt = opt_struc.get_space_group_info(
                    symprec=rin.symprec)
            except TypeError:
                spg_num_opt = 0
                spg_sym_opt = None
            # ------ out opt_struc
            out_poscar(opt_struc, self.cid, './data/opt_POSCARS')
            try:
                out_cif(opt_struc, self.cid, self.work_path,
                        './data/opt_CIFS.cif', rin.symprec)
            except TypeError:
                logger.warning('failed to write opt_CIF')
        # ---------- error
        else:
            spg_num_opt = 0
            spg_sym_opt = None
        # ---------- register opt_struc
        self.opt_struc_data[self.cid] = opt_struc
        pkl_data.save_opt_struc(self.opt_struc_data)
        # ---------- return
        return spg_sym, spg_num, spg_sym_opt, spg_num_opt

    def ctrl_next_struc(self):
        # ---------- RS
        if rin.algo == 'RS':
            next_struc_data = self.init_struc_data[self.cid]
        # ---------- BO
        elif rin.algo == 'BO':
            next_struc_data = self.init_struc_data[self.cid]
        # ---------- LAQA
        elif rin.algo == 'LAQA':
            if self.laqa_struc[self.cid]:    # vacant list?
                next_struc_data = self.laqa_struc[self.cid][-1]
            else:
                next_struc_data = self.init_struc_data[self.cid]
        # ---------- EA
        elif rin.algo in ['EA', 'EA-vc']:
            next_struc_data = self.init_struc_data[self.cid]
        # ---------- algo is wrong
        else:
            logger.error('Error, algo in ctrl_next_struc')
            raise SystemExit(1)
        # ---------- nat for EA-vc
        if rin.algo == 'EA-vc':
            nat = self.nat_data[self.cid]
        else:
            nat = rin.nat
        # ---------- common part
        # ------ in case there is no initial strucure data
        if next_struc_data is None:
            logger.info(f'ID {self.cid:>6}: initial structure is None')
            self.ctrl_skip()
        # ------ normal initial structure data
        else:
            # -- prepare input files for structure optimization
            if rin.kpt_flag:
                self.kpt_data = select_code.next_struc(next_struc_data,
                                                       self.cid,
                                                       self.work_path,
                                                       nat,
                                                       self.kpt_data)
            else:
                select_code.next_struc(next_struc_data, self.cid,
                                       self.work_path, nat)
            # -- prepare jobfile
            self.prepare_jobfile()
            # -- submit
            self.submit_next_struc()
            logger.info(f'ID {self.cid:>6}: submit job, Stage 1')
            # -- update status
            self.update_status(operation='submit')

    def submit_next_struc(self):
        # ---------- submit job
        os.chdir(self.work_path)    # cd work_path
        with open('stat_job', 'w') as fwstat:
            fwstat.write(f'{self.cid:<6}    # Structure ID\n')
            fwstat.write(f'{1:<6}    # Stage\n')
            fwstat.write('submitted\n')
        with open('sublog', 'w') as logf:
            subprocess.Popen([rin.jobcmd, rin.jobfile],
                             stdout=logf, stderr=logf)
        os.chdir('../../')    # go back to csp root dir

    def ctrl_skip(self):
        # ---------- log
        logger.info(f'ID {self.cid:>6}: Skip')
        # ---------- get initial spg info
        if self.init_struc_data[self.cid] is None:
            spg_sym = None
            spg_num = 0
        else:
            try:
                spg_sym, spg_num = self.init_struc_data[
                    self.cid].get_space_group_info(symprec=rin.symprec)
            except TypeError:
                spg_num = 0
                spg_sym = None
        # ---------- 'skip' for rslt
        spg_num_opt = 0
        spg_sym_opt = None
        energy = np.nan
        magmom = np.nan
        check_opt = 'skip'
        # ---------- register opt_struc
        self.opt_struc_data[self.cid] = None
        pkl_data.save_opt_struc(self.opt_struc_data)
        # ---------- RS
        if rin.algo == 'RS':
            # ------ save rslt
            self.rslt_data.loc[self.cid] = [spg_num, spg_sym,
                                            spg_num_opt, spg_sym_opt,
                                            energy, magmom, check_opt]
            pkl_data.save_rslt(self.rslt_data)
            out_rslt(self.rslt_data)
        # ---------- BO
        elif rin.algo == 'BO':
            # ------ save rslt
            self.rslt_data.loc[self.cid] = [self.n_selection,
                                            spg_num, spg_sym,
                                            spg_num_opt, spg_sym_opt,
                                            energy, magmom, check_opt]
            pkl_data.save_rslt(self.rslt_data)
            out_rslt(self.rslt_data)
            # ------ update descriptors
            self.opt_dscrpt_data[self.cid] = None
            # ------ save
            self.save_id_data()
            self.save_data()
        # ---------- LAQA
        elif rin.algo == 'LAQA':
            # ------ save rslt
            self.rslt_data.loc[self.cid] = [spg_num, spg_sym,
                                            spg_num_opt, spg_sym_opt,
                                            energy, magmom, check_opt]
            pkl_data.save_rslt(self.rslt_data)
            out_rslt(self.rslt_data)
            # ---------- laqa data
            self.laqa_step[self.cid].append(0)
            self.laqa_struc[self.cid].append(None)
            self.laqa_energy[self.cid].append(energy)
            self.laqa_bias[self.cid].append(np.nan)
            self.laqa_score[self.cid].append(-float('inf'))
            # ---------- save and out laqa data
            self.save_data()
            out_laqa_status(self.laqa_step, self.laqa_score,
                            self.laqa_energy, self.laqa_bias)
            out_laqa_step(self.laqa_step)
            out_laqa_score(self.laqa_score)
            out_laqa_energy(self.laqa_energy)
            out_laqa_bias(self.laqa_bias)
        # ---------- EA
        elif rin.algo == 'EA':
            self.rslt_data.loc[self.cid] = [self.gen,
                                            spg_num, spg_sym,
                                            spg_num_opt, spg_sym_opt,
                                            energy, magmom, check_opt]
            pkl_data.save_rslt(self.rslt_data)
            out_rslt(self.rslt_data)
        elif rin.algo == 'EA-vc':
            ef = np.nan
            self.rslt_data.loc[self.cid] = [self.gen,
                                            spg_num, spg_sym,
                                            spg_num_opt, spg_sym_opt,
                                            energy, ef, magmom, check_opt]
            pkl_data.save_rslt(self.rslt_data)
            out_rslt(self.rslt_data)
        # ---------- move to fin
        self.mv_fin()
        # ---------- update status
        self.update_status(operation='fin')
        # ---------- recheck
        self.recheck = True

    def update_status(self, operation):
        # ---------- update status
        if operation == 'submit':
            self.id_running.append(self.cid)
            self.id_queueing.remove(self.cid)
            io_stat.set_stage(self.stat, self.cid, 1)
        elif operation == 'fin':
            if self.cid in self.id_queueing:
                self.id_queueing.remove(self.cid)
            if self.cid in self.id_running:
                self.id_running.remove(self.cid)
            io_stat.clean_id(self.stat, self.cid)
        else:
            logger.error('operation is wrong')
            raise SystemExit(1)
        io_stat.set_id(self.stat, 'id_queueing', self.id_queueing)
        io_stat.write_stat(self.stat)
        # ---------- save id_data
        self.save_id_data()

    def prepare_jobfile(self):
        if not os.path.isfile('./calc_in/' + rin.jobfile):
            logger.error('Could not find ./calc_in' + rin.jobfile)
            raise SystemExit(1)
        with open('./calc_in/' + rin.jobfile, 'r') as f:
            lines = f.readlines()
        lines2 = []
        for line in lines:
            lines2.append(line.replace('CrySPY_ID', str(self.cid)))
        with open(self.work_path + rin.jobfile, 'w') as f:
            f.writelines(lines2)

    def mv_fin(self):
        if not os.path.isdir(f'work/fin/{self.cid:06}'):
            shutil.move(f'work/{self.cid:06}', 'work/fin/')
        else:    # rename for recalc
            for i in itertools.count(1):
                if not os.path.isdir(f'work/fin/{self.cid:06}_{i}'):
                    shutil.move(f'work/{self.cid:06}',
                                f'work/fin/{self.cid:06}_{i}')
                    break

    def next_sg(self, noprint=False):
        '''
        next selection or generation
        '''
        if rin.algo == 'BO':
            self.next_select_BO(noprint)
        if rin.algo == 'LAQA':
            self.next_select_LAQA()
        if rin.algo in ['EA', 'EA-vc']:
            self.next_gen_EA()

    def next_select_BO(self, noprint=False):
        # ---------- log
        logger.info(f'\nDone selection {self.n_selection}')
        # ---------- done all structures
        if len(self.rslt_data) == rin.tot_struc:
            logger.info('\nDone all structures!')
            os.remove('lock_cryspy')
            raise SystemExit()
        # ---------- flag for next selection or generation
        if not self.go_next_sg:
            logger.info('\nBO is ready')
            os.remove('lock_cryspy')
            raise SystemExit()
        # ---------- check point 3
        if rin.stop_chkpt == 3:
            logger.info('\nStop at check point 3: BO is ready')
            os.remove('lock_cryspy')
            raise SystemExit()
        # ---------- max_select_bo
        if 0 < rin.max_select_bo <= self.n_selection:
            logger.info(f'\nReached max_select_bo: {rin.max_select_bo}')
            os.remove('lock_cryspy')
            raise SystemExit()
        # ---------- BO
        backup_cryspy()
        bo_data = (self.init_dscrpt_data, self.opt_dscrpt_data,
                   self.bo_mean, self.bo_var, self.bo_score)
        bo_id_data = (self.n_selection, self.id_queueing,
                      self.id_running, self.id_select_hist)
        bo_next_select.next_select(self.stat, self.rslt_data,
                                   bo_id_data, bo_data, noprint)

    def next_select_LAQA(self):
        # ---------- flag for next selection or generation
        if not self.go_next_sg:
            logger.info('\nLAQA is ready')
            os.remove('lock_cryspy')
            raise SystemExit()
        # ---------- check point 3
        if rin.stop_chkpt == 3:
            logger.info('\nStop at check point 3: LAQA is ready')
            os.remove('lock_cryspy')
            raise SystemExit()
        # ---------- selection of LAQA
        backup_cryspy()
        laqa_id_data = (self.id_queueing, self.id_running,
                        self.id_select_hist)
        laqa_data = (self.tot_step_select, self.laqa_step, self.laqa_struc,
                     self.laqa_energy, self.laqa_bias, self.laqa_score)
        laqa_next_selection.next_selection(self.stat, laqa_id_data, laqa_data)

    def next_gen_EA(self):
        # ---------- log
        logger.info(f'Done generation {self.gen}')
        # ---------- flag for next selection or generation
        if not self.go_next_sg:
            logger.info('\nEA is ready')
            os.remove('lock_cryspy')
            raise SystemExit()
        # ---------- check point 3
        if rin.stop_chkpt == 3:
            logger.info('\nStop at check point 3: EA is ready')
            os.remove('lock_cryspy')
            raise SystemExit()
        # ---------- maxgen_ea
        if 0 < rin.maxgen_ea <= self.gen:
            if rin.algo == 'EA-vc':
                # ------ when gen reaches maxgen_ea,  next generation is not created
                #        so convex hull is calculated here
                #        update only convex hull and hdist, not elite_struc and elite_fitness
                c_rslt = self.rslt_data[self.rslt_data['Gen'] == self.gen]
                c_ids = c_rslt.index.values    # current IDs [array]
                ef_all = self.rslt_data['Ef_eV_atom'].to_dict()    # formation energy of all structures
                hdist = calc_convex_hull_2d(self.ratio_data, ef_all, c_ids, self.gen)
                out_hdist(self.gen, hdist, self.ratio_data)
                self.hdist_data[self.gen] = hdist
                ea_vc_data = (self.nat_data, self.ratio_data, self.hdist_data)
                pkl_data.save_ea_vc_data(ea_vc_data)
            logger.info(f'\nReached maxgen_ea: {rin.maxgen_ea}')
            os.remove('lock_cryspy')
            raise SystemExit()
        # ---------- EA
        backup_cryspy()
        ea_id_data = (self.gen, self.id_queueing, self.id_running)
        if rin.struc_mode in ['mol', 'mol_bs']:
            struc_mol_id = self.struc_mol_id
        else:
            struc_mol_id = None
        if rin.algo == 'EA-vc':
            ea_vc_data = (self.nat_data, self.ratio_data, self.hdist_data)
        else:
            ea_vc_data = None
        ea_next_gen.next_gen(self.stat, self.init_struc_data, struc_mol_id,
                             self.opt_struc_data, self.rslt_data, ea_id_data, ea_vc_data)

    def save_id_data(self):
        # ---------- save id_data
        if rin.algo == 'RS':
            rs_id_data = (self.id_queueing, self.id_running)
            pkl_data.save_rs_id(rs_id_data)
        if rin.algo == 'BO':
            bo_id_data = (self.n_selection, self.id_queueing,
                          self.id_running, self.id_select_hist)
            pkl_data.save_bo_id(bo_id_data)
        if rin.algo == 'LAQA':
            laqa_id_data = (self.id_queueing, self.id_running,
                            self.id_select_hist)
            pkl_data.save_laqa_id(laqa_id_data)
        if rin.algo in ['EA', 'EA-vc']:
            ea_id_data = (self.gen, self.id_queueing, self.id_running)
            pkl_data.save_ea_id(ea_id_data)

    def save_data(self):
        # ---------- save ??_data
        if rin.algo == 'BO':
            bo_data = (self.init_dscrpt_data, self.opt_dscrpt_data,
                       self.bo_mean, self.bo_var, self.bo_score)
            pkl_data.save_bo_data(bo_data)
        if rin.algo == 'LAQA':
            laqa_data = (self.tot_step_select, self.laqa_step, self.laqa_struc,
                         self.laqa_energy, self.laqa_bias, self.laqa_score)
            pkl_data.save_laqa_data(laqa_data)
        # ea_data is used only in ea_next_gen.py
        # ea_vc_data is used in this class, but it is not updated.
        # ea_vc_data is saved in ea_next_gen.py
