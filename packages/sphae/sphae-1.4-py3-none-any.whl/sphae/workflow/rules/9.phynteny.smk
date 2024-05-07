"""
Running phynteny to improve the anntoation 
"""
rule phynteny_run_paired:
    input:
        gbk=os.path.join(dir.pharokka,"{sample}-pr-phold","{sample}.gbk")
    params:
        odir=os.path.join(dir.pharokka, "{sample}-pr", "phynteny"),
        model=os.path.join(dir.db, "phynteny_models_zenodo")
    output:
        pkl=os.path.join(dir.pharokka, "{sample}-pr", "phynteny", "phynteny.gbk")
    conda:
        os.path.join(dir.env, "phynteny.yaml")
    threads:
        config.resources.smalljob.cpu
    resources:
        mem_mb = config.resources.smalljob.mem,
        time = config.resources.smalljob.time
    log:
        os.path.join(dir.log, "phynteny.{sample}.log")
    benchmark:
        os.path.join(dir.bench,"phynteny_megahit_{sample}.txt")
    shell:
        """
        if [[ -s {input.gbk} ]] ; then
            phynteny {input.gbk} -o {params.odir} \
                -m {params.model} -f\
                2> {log}
            touch {output.pkl}
        else
            touch {output.pkl}
        fi
        """

rule phynteny_run_nanopore:
    input:
        gbk=os.path.join(dir.pharokka,"{sample}-sr-phold","{sample}.gbk")
    params:
        odir=os.path.join(dir.pharokka, "{sample}-sr", "phynteny"),
        model=os.path.join(dir.db, "phynteny_models_zenodo")
    output:
        pkl=os.path.join(dir.pharokka, "{sample}-sr", "phynteny", "phynteny.gbk")
    conda:
        os.path.join(dir.env, "phynteny.yaml")
    threads:
        config.resources.smalljob.cpu
    resources:
        mem_mb = config.resources.smalljob.mem,
        time = config.resources.smalljob.time
    log:
        os.path.join(dir.log, "phynteny.{sample}.log")
    benchmark:
        os.path.join(dir.bench,"phynteny_nanopore_{sample}.txt")
    shell:
        """
        if [[ -s {input.gbk} ]] ; then
            phynteny {input.gbk} -o {params.odir} \
                -m {params.model} -f\
                2> {log}
            touch {output.pkl}
        else
            touch {output.pkl}
        fi
        """
