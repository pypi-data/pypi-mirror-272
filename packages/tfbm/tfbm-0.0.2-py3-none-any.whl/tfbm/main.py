from .load_data import load_atoms_synthetic_data
from .TFBM import TFBM

if __name__ == '__main__':
    data, spectrumData = load_atoms_synthetic_data()
    tfbm = TFBM(data.T, threshold="auto", merge=True, aspect_ratio=1, merge_factor=15)
    tfbm.fit(verbose=True, timer=True)

    tfbm.plot_result("TFBM", data, tfbm.merged_labels_data.T, tfbm.packet_infos)
