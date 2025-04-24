# QEST+FORMATS 2025 artifact

This directory contains the artifact corresponding to the paper "Numerical stability of quantitative system analysis using decision diagrams", submitted to QEST+FORMATS 2025. The following is included:
* Usage instructions (this document).
* The DD package Q-Sylvan, in `mtbdd-benchmarks/tools/q-sylvan/` (also available online at https://github.com/System-Verification-Lab/Q-Sylvan).
* Quantum circuits in the OpenQASM format used for benchmarks, in `mtbdd-benchmarks/qasm/`.
* Python scripts for setting up and processing benchmarks, in `mtbdd-benchmarks/scripts/`.

This artifact has been tested on Ubuntu 24.04 and on Windows 11 using WSL 2.


## 1. Docker instructions

NOTE: In the [Docker image](https://doi.org/10.5281/zenodo.15274872) all required dependencies are preinstalled. When not using this repository from the Docker image, dependency installation instructions can be found in [`dependencies.md`](dependencies.md).


* In the following, `#` indicates commands run in the the Docker container, and `$` indicates commands run in the host shell.
* Depending on the system, `docker` might need to be run as `sudo docker` in the commands below.

1\. Create a new Docker container from the given Docker image. The last command should show the new container with the name "qf25-artifact".
```
$ docker load < qf25-artifact-img.tar
$ docker run --name qf25-artifact -it qf25-artifact-img:v1.0 bash
# exit
$ docker ps -a
```

2\. Enter the Docker container and compile the source:
```
$ docker start qf25-artifact
$ docker exec -it qf25-artifact bash
# cd /mtbdd-benchmarks/
# source .venv/bin/activate
# ./compile_all.sh -qr
```

3\. To retrieve all output (include figures) from the Docker container, run the following on the host shell.
```
$ docker cp qf25-artifact:/mtbdd-benchmarks/experiments/ .
```


## 2. Running + plotting

In the following we specify the plots can be reproduced.
Running the full benchmarks can take several days.
Because of this, we also include instructions on how to run a small subset of benchmarks that can run in a few minutes.
The commands are supposed to be run from the root of the `mtbdd-benchmarks` directory.

### Subset (~10 minutes compute time per figure)

#### Figure 2:
```
# python scripts/generate_sim_experiments.py qasm/mqtbench_indep/ --name mtbdd_qcsim_53_subset --from_list qasm/mtbdd_quick_eval_selection.txt --precisions 53 --log_vector --tolerances 0 1e-19 1e-15 1e-11 1e-7 1e-3

# bash experiments/mtbdd_qcsim_53_subset/run_all.sh

# python scripts/process_results.py experiments/mtbdd_qcsim_53_subset
```
After running the commands above, the plots can be found in
* errors: `experiments/mtbdd_qcsim_53_subset/plots/heatmaps/circuit_type_precision_max_error_abs/complete/png`
* node counts: `experiments/mtbdd_qcsim_53_subset/plots/heatmaps/circuit_type_precision_max_error_abs/complete/png`


#### Figure 3:
```
# python scripts/generate_sim_experiments.py qasm/mqtbench_indep/ --name mtbdd_qcsim_24_subset --from_list qasm/mtbdd_quick_eval_selection.txt --precisions 24 --log_vector --tolerances 0 1e-19 1e-15 1e-11 1e-7 1e-3

# bash experiments/mtbdd_qcsim_24_subset/run_all.sh

# python scripts/process_results.py experiments/mtbdd_qcsim_24_subset
```
After running the commands above, the plots can be found in
* errors: `experiments/mtbdd_qcsim_24_subset/plots/heatmaps/circuit_type_precision_max_error_abs/complete/png`
* node counts: `experiments/mtbdd_qcsim_24_subset/plots/heatmaps/circuit_type_precision_max_error_abs/complete/png`


### Full benchmarks (~1 or 2 days compute time per figure)


#### Figure 2:
```
# python scripts/generate_sim_experiments.py qasm/mqtbench_indep/ --name mtbdd_qcsim_53 --from_list qasm/mtbdd_selection.txt --precisions 53 --log_vector --tolerances 0 1e-19 1e-18 1e-17 1e-16 1e-15 1e-14 1e-13 1e-12 1e-11 1e-10 1e-9 1e-8 1e-7 1e-6 1e-5 1e-4 1e-3

# bash experiments/mtbdd_qcsim_53/run_all.sh

# python scripts/process_results.py experiments/mtbdd_qcsim_53
```
After running the commands above, the plots can be found in
* errors: `experiments/mtbdd_qcsim_53/plots/heatmaps/circuit_type_precision_max_error_abs/complete/png`
* node counts: `experiments/mtbdd_qcsim_53/plots/heatmaps/circuit_type_precision_max_error_abs/complete/png`


#### Figure 3:
```
# python scripts/generate_sim_experiments.py qasm/mqtbench_indep/ --name mtbdd_qcsim_24 --from_list qasm/mtbdd_selection.txt --precisions 24 --log_vector --tolerances 0 1e-19 1e-18 1e-17 1e-16 1e-15 1e-14 1e-13 1e-12 1e-11 1e-10 1e-9 1e-8 1e-7 1e-6 1e-5 1e-4 1e-3

# bash experiments/mtbdd_qcsim_24/run_all.sh

# python scripts/process_results.py experiments/mtbdd_qcsim_24
```
After running the commands above, the plots can be found in
* errors: `experiments/mtbdd_qcsim_24/plots/heatmaps/circuit_type_precision_max_error_abs/complete/png`
* node counts: `experiments/mtbdd_qcsim_24/plots/heatmaps/circuit_type_precision_max_error_abs/complete/png`
