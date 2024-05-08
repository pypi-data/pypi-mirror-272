# Time-Frequency Breakdown Method
The Time-Frequency Breakdown Method (TFBM) was developed for the detection of brain oscillations in time-frequency representations (such as spectrograms obtained from the Fourier Transform) and was published in Frontiers in Human Neuroscience:
https://www.frontiersin.org/articles/10.3389/fnhum.2023.1112415/full

![TFBM](/images/tfbm.png?raw=true)

# Install:
```
pip install tfbm
```

Usage example:
```
from load_data import load_atoms_synthetic_data
from tfbm import TFBM

if __name__ == '__main__':
    data, spectrumData = load_atoms_synthetic_data()
    tfbm = TFBM(data.T, threshold="auto", merge=True, aspect_ratio=1, merge_factor=15)
    tfbm.fit(verbose=True, timer=True)

    tfbm.plot_result("TFBM", data, tfbm.merged_labels_data.T, tfbm.packet_infos)

```

# Citations
We would appreciate it, if you cite the paper when you use this work for the TFBM algorithm:

- For Plain Text:
```
E.-R. Ardelean, H. Bârzan, A.-M. Ichim, R. C. Mureşan, and V. V. Moca, “Sharp detection of oscillation packets in rich time-frequency representations of neural signals,” Frontiers in Human Neuroscience, vol. 17, 2023, doi: 10.3389/fnhum.2023.1112415.
```

- BibTex:
```
@ARTICLE{10.3389/fnhum.2023.1112415,
AUTHOR={Ardelean, Eugen-Richard and Bârzan, Harald and Ichim, Ana-Maria and Mureşan, Raul Cristian and Moca, Vasile Vlad},   
TITLE={Sharp detection of oscillation packets in rich time-frequency representations of neural signals},      
JOURNAL={Frontiers in Human Neuroscience},      
VOLUME={17},           
YEAR={2023},      
URL={https://www.frontiersin.org/articles/10.3389/fnhum.2023.1112415},       
DOI={10.3389/fnhum.2023.1112415}
}
```

# Contact
If you have any questions about SBM, feel free to contact me. (Email: ardeleaneugenrichard@gmail.com)
