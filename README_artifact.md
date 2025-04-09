# QEST+FORMATS 2025 artifact

This directory contains the artifact corresponding to the paper "...", submitted to QEST+FORMATS 2025. The following is included:
* Usage instructions (this document).
* The DD package Q-Sylvan, in `tools/q-sylvan/` (also available online at https://github.com/System-Verification-Lab/Q-Sylvan).
* Quantum circuits in the OpenQASM format used for benchmarks, in `qasm/`.
* Python scripts for setting up and processing benchmarks, in `scripts/`.



## 1. Docker instructions

TODO


## 2. Running + plotting

In the following we specify the plots can be reproduced.
Running the full benchmarks can take several days.
Because of this, we also include instructions on how to run a small subset of benchmarks that can run in a few minutes. 

### Subset (?? minutes compute time per figure)

Figure 2:
```shell
python scripts/generate_sim_experiments.py qasm/mqtbench_indep/ --name mtbdd_qcsim_53_subset --from_list qasm/mtbdd_quick_eval_selection.txt --precisions 53 --log_vector --tolerances 0 1e-19 1e-17 1e-15 1e-13 1e-11 1e-9 1e-7 1e-5 1e-3

bash experiments/mtbdd_qcsim_53_subset/run_all.sh

python scripts/process_results.py experiments/mtbdd_qcsim_53_subset
```

Figure 3:
```shell
python scripts/generate_sim_experiments.py qasm/mqtbench_indep/ --name mtbdd_qcsim_24_subset --from_list qasm/mtbdd_quick_eval_selection.txt --precisions 24 --log_vector --tolerances 0 1e-19 1e-17 1e-15 1e-13 1e-11 1e-9 1e-7 1e-5 1e-3

bash experiments/mtbdd_qcsim_24_subset/run_all.sh

python scripts/process_results.py experiments/mtbdd_qcsim_24_subset
```


### Full benchmarks (~1 or 2 days compute time per figure)


Figure 2:
```shell
python scripts/generate_sim_experiments.py qasm/mqtbench_indep/ --name mtbdd_qcsim_53 --from_list qasm/mtbdd_selection.txt --precisions 53 --log_vector --tolerances 0 1e-19 1e-18 1e-17 1e-16 1e-15 1e-14 1e-13 1e-12 1e-11 1e-10 1e-9 1e-8 1e-7 1e-6 1e-5 1e-4 1e-3

bash experiments/mtbdd_qcsim_53/run_all.sh

python scripts/process_results.py experiments/mtbdd_qcsim_53
```

Figure 3:
```shell
python scripts/generate_sim_experiments.py qasm/mqtbench_indep/ --name mtbdd_qcsim_24 --from_list qasm/mtbdd_selection.txt --precisions 24 --log_vector --tolerances 0 1e-19 1e-18 1e-17 1e-16 1e-15 1e-14 1e-13 1e-12 1e-11 1e-10 1e-9 1e-8 1e-7 1e-6 1e-5 1e-4 1e-3

bash experiments/mtbdd_qcsim_24/run_all.sh

python scripts/process_results.py experiments/mtbdd_qcsim_24
```




