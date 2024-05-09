# BSD 3-Clause License
#
# Copyright (c) 2021, Austin Cummings
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# TODO: make Showerfile actually configurable, requires calculation of X_0 and energy of shower file

''' IO Functions

.. autosummary::
   :toctree:
   :recursive:

   CORSIKA_Shower_Reader
   average_CORSIKA_profile
   read_config

'''

from rich.console import Console
from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from importlib_resources import files
from os.path import exists as file_exists

import configparser as cp
import numpy as np
import io
import sys

import matplotlib.pyplot as plt

try:
    from ROOT import TFile, TTree, TH1D, vector
except ImportError:
    root_found = False
else:
    root_found = True


class IO:
    """root IO class
    """
    def __init__(self, file_name='CherSim.root'):
        self.check_file_exist(file_name)
        self.__filename = file_name
        self.__root = False
        if ".root" in file_name:
            self.__root = True
            self.__vec_time = vector("TH1D")()
            self.__vec_phZenith = vector("TH1D")()
            self.__vec_phAzi = vector("TH1D")()
            self.create_root_file(file_name)

    def check_file_exist(self, file_name):
        if file_exists(file_name):
            overwrite = get_console().input(f'''[bold blue]WARN:[/] A file with the same name'''
                                            f''' [italic]{file_name}[/] already exist.'''
                                            f''' Do you want to overwrite it? (yes/no) ''')
            if 'y' not in overwrite.lower():
                sys.exit(0)
        flog(f'''Simulation result will be written to {file_name} \n''')

    def create_root_file(self, filename):
        self.__file = TFile(filename, 'recreate')
        self.__tcher_ph = TTree("cherPhProp", "Cherenkov Photon Properties")
        self.__tshower = TTree("showerProp", "Shower Properties")

        # create branches for tshower
        self.__eng = np.zeros(1, dtype=float)
        self.__zen = np.zeros(1, dtype=float)
        self.__startdist = np.zeros(1, dtype=float)
        self.__X0 = np.zeros(1, dtype=float)

        self.__tshower.Branch("energy", self.__eng, 'eng/D')
        self.__tshower.Branch("zenith", self.__zen, 'zen/D')
        self.__tshower.Branch("startdist", self.__startdist, 'startdist/D')
        self.__tshower.Branch("X0", self.__X0, 'X0/D')

        # define histograms
        histo_w = TH1D()
        histo_r = TH1D()
        histo_t_off = TH1D()
        histo_phZenith_off = TH1D()

        # set branch for histograms
        self.__tcher_ph.Branch("wavelength", 'TH1D', histo_w)
        self.__tcher_ph.Branch("distance", 'TH1D', histo_r)
        self.__tcher_ph.Branch("time_offset", 'TH1D', histo_t_off)
        self.__tcher_ph.Branch("phZenith_offset", 'TH1D', histo_phZenith_off)
        self.__tcher_ph.Branch("time_dist", self.__vec_time)
        self.__tcher_ph.Branch("phZenith_dist", self.__vec_phZenith)
        self.__tcher_ph.Branch("phAzimuth_dist", self.__vec_phAzi)

    def write_shower_prop(self, energy, theta_D, L_particle, X0):
        # add shower properties
        self.__shower_settings = np.array([energy, theta_D, L_particle, X0], dtype=float)
        if self.__root:
            self.__eng[0] = energy
            self.__zen[0] = theta_D
            self.__startdist[0] = L_particle
            self.__X0[0] = X0
            self.__tshower.Fill()

    def write_cher_ph_prop(self, cher_ph):

        if self.__root:
            num_wl_bin = len(cher_ph["wavelengths"]) - 1
            num_dist_bin = len(cher_ph["r_bins"]) - 1
            num_time_bin = len(cher_ph["time_bins"]) - 1
            num_phZenith_bin = len(cher_ph["phZenith_bins"]) - 1
            num_phAzi_bin = len(cher_ph["phAzi_bins"]) - 1

            # define histograms
            histo_w = TH1D("wl", "wavelength", num_wl_bin, cher_ph["wavelengths"])
            histo_r = TH1D("r", "distance", num_dist_bin, cher_ph["r_bins"])
            histo_t_off = TH1D("t_off", "time offset",
                                num_dist_bin, cher_ph["r_bins"])
            histo_phZenith_off = TH1D("phZenith_off", "phZenith offset",
                                    num_dist_bin, cher_ph["r_bins"])
            histo_t = [
                TH1D(
                    f"t_dist_{str(i)}",
                    f"time_dist_{str(i)}",
                    num_time_bin,
                    cher_ph["time_bins"],
                )
                for i in range(num_dist_bin)
            ]
            histo_phZenith = [
                TH1D(
                    f"phZenith_dist_{str(i)}",
                    f"phZenith_dist_{str(i)}",
                    num_phZenith_bin,
                    cher_ph["phZenith_bins"],
                )
                for i in range(num_dist_bin)
            ]

            histo_phAzi = [
                TH1D(
                    f"phAzi_dist_{str(i)}",
                    f"phAzi_dist_{str(i)}",
                    num_phAzi_bin,
                    cher_ph["phAzi_bins"],
                )
                for i in range(num_dist_bin)
            ]

            # fill histograms
            for wl_bin, counts in enumerate(cher_ph["wavelength_counts"]):
                histo_w.SetBinContent(wl_bin + 1, counts)
            for r_bin, counts in enumerate(cher_ph["r_counts"]):
                histo_r.SetBinContent(r_bin + 1, counts)
                histo_t_off.SetBinContent(r_bin + 1, cher_ph["lower_times"][r_bin])
                histo_phZenith_off.SetBinContent(r_bin + 1, cher_ph["lower_phZenith"][r_bin])
                for t_bin, counts_t in enumerate(cher_ph["time_counts"][r_bin]):
                    histo_t[r_bin].SetBinContent(t_bin + 1, counts_t)
                for phZenith_bin, counts_phZenith in enumerate(cher_ph["phZenith_counts"][r_bin]):
                    histo_phZenith[r_bin].SetBinContent(phZenith_bin + 1, counts_phZenith)
                for phAzi_bin, counts_phAzi in enumerate(cher_ph["phAzi_counts"][r_bin]):
                    histo_phAzi[r_bin].SetBinContent(phAzi_bin + 1, counts_phAzi)

            self.__tcher_ph.SetBranchAddress("wavelength", histo_w)
            self.__tcher_ph.SetBranchAddress("distance", histo_r)
            self.__tcher_ph.SetBranchAddress("phZenith_offset", histo_phZenith_off)
            self.__tcher_ph.SetBranchAddress("time_offset", histo_t_off)
            self.__vec_time.assign(histo_t)
            self.__vec_phZenith.assign(histo_phZenith)
            self.__vec_phAzi.assign(histo_phAzi)
            self.__tcher_ph.Fill()
        else:
            np.savez(self.__filename, shower_prop=self.__shower_settings,
                     wavelengths=cher_ph["wavelengths"], wavelength_counts=cher_ph["wavelength_counts"],
                     dist_bins=cher_ph["r_bins"], dist_counts=cher_ph["r_counts"],
                     time_bins=cher_ph["time_bins"], time_counts=cher_ph["time_counts"],
                     time_offset=cher_ph["lower_times"],
                     phZenith_bins=cher_ph["phZenith_bins"], phZenith_counts=cher_ph["phZenith_counts"],
                     phZenith_offset=cher_ph["lower_phZenith"],
                     phAzi_bins=cher_ph["phAzi_bins"], phAzi_counts=cher_ph["phAzi_counts"],
                     t_counts=cher_ph["t_counts"],
                    )

    def close(self):
        if self.__root:
            self.__tshower.Write("", TFile.kOverwrite)
            self.__tcher_ph.Write("", TFile.kOverwrite)
            self.__file.Close()


def is_float(s):
    """Determines if an input value is a float

    Parameters
    ----------
    s : str
        input string

    Returns
    -------
    Boolean
        True: if string is float, False otherwise
    """

    try:
        float(s)
        return True
    except ValueError:
        return False


def CORSIKA_Shower_Reader(filename):
    """Reads in longitudinal charged particle profiles (.long files) generated by CORSIKA simulations

    Parameters
    ----------
    filename : str
        CORSIKA .long file path

    Returns
    -------
    ArrayLike
        longitudial charged particle profile of showers array of lists (depth, number of electrons)
    """
    # Initialize an array to contain all the simulated showers and arrays to contain the depths (g/cm^2) and particle content for each shower
    showers = []
    depths, electrons = [], []

    with open(filename) as f:
        # Flag for whether to output the lines which follow, initialize as false
        readout_flag = False

        # Loop through the given file line by line
        for line in f:
            if readout_flag:

                # Split the line on the " " delimiter
                data = line.split()
                # If the first value is a float, can continue
                if is_float(data[0]):
                    # Append the depth to the depth array, and the sum of electrons and positrons to the electron array
                    # If other particle types are desired:
                    # [0]: depths, [1]: gammas, [2]: electrons, [3]: positrons, [4]: anti-muons, [5]: muons, [6]: hadrons, [7]: charged particles, [8]: nuclei
                    depths.append(float(data[0]))
                    electrons.append(float(data[2]) + float(data[3]))

            # Determine if charged particle info follows.
            # CORSIKA outputs charged particle profiles, followed by energy information, so flag must switch every instance of header
            if ("ELECTRONS" in line) or ("EM CUT" in line):
                # Append shower info to container array
                if len(depths) > 0:
                    showers.append([depths, electrons])

                readout_flag = not readout_flag
                # Reinitialize arrays
                depths, electrons = [], []

    return np.array(showers)


def average_CORSIKA_profile(showers):
    """Calculates the average charged particle longitudinal profile from the CORSIKA data

    Parameters
    ----------
    showers : ArrayLike
        array of showers returned by the CORSIKA_Shower_Reader function

    Returns
    -------
    ArrayLike
        the average longitudinal charged particle profile of many showers
    """
    return np.average(showers, axis=0)

def average_CORSIKA_profile_2(showers):
    """Calculates the average charged particle longitudinal profile from the CORSIKA data

    Parameters
    ----------
    showers : ArrayLike
        array of showers returned by the CORSIKA_Shower_Reader function

    Returns
    -------
    ArrayLike
        the average longitudinal charged particle profile of many showers
    """
    indices = np.argmax(showers[:,1,:], axis = 1)
    min_index = np.min(indices)

    shifts = indices-min_index
    new_parts = np.array([np.roll(showers[i,1,:], -shifts[i]) for i in range(len(shifts))])
    
    showers[:, 1, :] = new_parts
    
    fig = plt.figure()
    for i in range(len(shifts)):
        
        plt.plot(showers[i,0,:], showers[i, 1, :], color = 'red')
    
    #average_shower = np.array([showers[loc_min_index, 0, :], showers[loc_min_index, 1, :]])
    average_shower = np.average(showers, axis=0)
    plt.plot(showers[i,0,:], average_shower[1,:], label = 'Average Profile', color = 'black')
    plt.xlabel('Grammage '+r'$(\mathrm{g}/\mathrm{cm}^{2})$')
    plt.ylabel('Charged Particles')
    plt.yscale('log')
    #plt.show()
    
    #
    '''
    plt.plot(average_shower[0], average_shower[1], color = 'black')
    plt.yscale('log')
    plt.show()
'''
    return average_shower

def read_config(cfg_file):
    """Read configuration file.

    Parameters
    ----------
    cfg_file : str
        name of User config file

    Returns
    -------
    ConfigParser
        Settings for simulation (defualt & user specified)
    """
    cfg = cp.ConfigParser(allow_no_value=True,
                          converters={'list': lambda x: [i.strip() for i in x.split(',')]})
    cfg.optionxform = lambda option: option
    # read default settings
    default_cfg = files("easchersim.data")/"default_conf.ini"
    cfg.read(default_cfg)

    # read user settings (overwrittes defaults)
    cfg.read(cfg_file)

    return cfg


def create_config(user_args):
    """Creates example configuration file

    Values can be specified by user via command line all not specified parameter will be default

    Parameters
    ----------
    user_args : namespace
        User inputs parsed by argparse
    """
    cfg = cp.ConfigParser()
    cfg.optionxform = lambda option: option
    cfg['shower'] = {'energy': user_args.eng,
                     'X0': user_args.X0,
                     'angle': f"""{user_args.angle[0]}, {user_args.angle[1]}""",
                     'distFirstInt': f"""{user_args.distFirstInt[0]}, {user_args.distFirstInt[1]}"""}
    cfg['detector'] = {'altitude': user_args.det_alt}
    cfg['atmosphere'] = {'scattering': user_args.atm_scatter}
    cfg['magField'] = {'useField': user_args.mag_field}
    cfg['runSettings'] = {'useGreisenParametrization': user_args.useGreisen,
                          'lat_dist': user_args.lat_dist}
    cfg['output'] = {'name': user_args.output_name,
                     'plots': user_args.plots,
                     'saveFigures': "yes" if user_args.savefig else "no"}

    with open(user_args.filename, 'w') as cfg_file:
        cfg.write(cfg_file)


def dump_default_conf():
    """Print default configuration to screen
    """
    cfg = cp.ConfigParser()
    # read default settings
    default_cfg = files("easchersim.data")/"default_conf.ini"
    cfg.read(default_cfg)
    with io.StringIO() as str_stream:
        cfg.write(str_stream)
        print(str_stream.getvalue())


def get_console(**kargs):
    return (
        Console(**kargs, width=100)
        if kargs
        else Console(width=100, log_path=False)
    )


def flog(*args):
    get_console().log(*args)


def get_progress():
    text_col = TextColumn("[bold red]{task.description}", table_column=Column(ratio=1))
    bar_col = BarColumn(bar_width=40, table_column=Column(ratio=4))

    return Progress(
        text_col,
        bar_col,
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        console=get_console(),
    )
