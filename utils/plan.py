import numpy as np
import scipy
from utils import load_metadata, load_data
from .beam import Beam, Beams
from .structures import Structures
import os
import pandas as pd


class Plan(object):
    """
    A class representing plan for given beams.
    """

    # def __init__(self, ID, gantry_angle=None, collimator_angle=None, iso_center=None, beamlet_map_2d=None,
    #              BEV_structure_mask=None, beamlet_width_mm=None, beamlet_height_mm=None, beam_modality=None, MLC_type=None):
    def __init__(self, patient_name, beam_indices=None, options=None):

        # patient_name = 'ECHO_PROST_1'
        patient_folder_path = os.path.join(os.getcwd(), "..", 'Data', patient_name)
        # read all the meta data for the required patient
        meta_data = load_metadata(patient_folder_path)

        # load data for the given beam_indices
        if len(options) != 0:
            if 'loadInfluenceMatrixFull' in options and not options['loadInfluenceMatrixFull']:
                meta_data['beams']['influenceMatrixFull_File'] = [None] * len(
                    meta_data['beams']['influenceMatrixFull_File'])
            if 'loadInfluenceMatrixSparse' in options and not options['loadInfluenceMatrixSparse']:
                meta_data['beams']['influenceMatrixSparse_File'] = [None] * len(
                    meta_data['beams']['influenceMatrixSparse_File'])
            if 'loadBeamEyeViewStructureMask' in options and not options['loadBeamEyeViewStructureMask']:
                meta_data['beams']['beamEyeViewStructureMask_File'] = [None] * len(
                    meta_data['beams']['beamEyeViewStructureMask_File'])

        if beam_indices is None:
            beam_indices = [0, 10, 20, 30]
        my_plan = meta_data.copy()
        del my_plan['beams']
        beamReq = dict()
        inds = []
        for i in range(len(beam_indices)):
            if beam_indices[i] in meta_data['beams']['ID']:
                ind = np.where(np.array(meta_data['beams']['ID']) == beam_indices[i])
                ind = ind[0][0]
                inds.append(ind)
                for key in meta_data['beams']:
                    beamReq.setdefault(key, []).append(meta_data['beams'][key][ind])
        my_plan['beams'] = beamReq
        if len(inds) < len(beam_indices):
            print('some indices are not available')
        my_plan = load_data(my_plan, my_plan['patient_folder_path'])
        # df = pd.DataFrame.from_dict(my_plan['beams'])
        # self.beam = [Beam(df.loc[i]) for i in range(len(beam_indices))]
        self.beams = Beams(my_plan['beams'])
        self.structures = Structures(my_plan['structures'], my_plan['opt_voxels'])