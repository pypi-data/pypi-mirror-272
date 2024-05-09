![TALP LOGO](talp_dlb_logo.png){height=250px}

# Talp Pages

TALP Pages is a collection of Python scripts to postprocess the `json` outputs of [DLB TALP](https://pm.bsc.es/ftp/dlb/doc/user-guide/intro.html#talp-tracking-application-live-performance) and Gitlab pipeline snippets [that can be included](https://docs.gitlab.com/ee/ci/yaml/#include) in your project.
This makes it easy to integrate TALP into your CI/CD setup and run Continous Benchmarking without having to code up your own solution.

**We provide:**

- talp_pages: Command line tool to generate static html pages
- Artifact management: A easy way to use Gitlab Artifacts to generate time series data plots.
- Reusable Jobs that easily integrate into a existing Gitlab CI enviroment

## Use python package

Talp-Pages is written in Python (3.9+). We rely on [poetry](https://python-poetry.org/) for packaging.
To use, simply install via:

```pip install talp-pages```

From there you should have the following command-line tools available:

- `talp_report`
- `talp_add_to_db`
- `talp_badge`
- `talp_report_ts`
- `talp_pages`
- `talp_download_artifacts`

## Use Gitlab Jobs

This section currently is not completly done, but we provide examples on how to use the jobs below:

```yaml

talp-performance-run:
  stage: performance
  image: python:3.12-bullseye
  script:
    - python generate_talp_json.py
  artifacts:
    paths:
      - talp.json


include:
  - remote: https://pm.bsc.es/gitlab/dlb/talp-pages/-/raw/main/templates/add-to-db/template.yml
    inputs:
      stage: deploy
      generating_job: talp-performance-run
      talp_output: ./talp.json
      enviroment: production
      gitlab_url: https://gitlab.com
      project_name: valentin.seitz1/sample-application
      dlb_home: ./dlb_talp
      job_name: talp-create-artifacts
  - remote: https://pm.bsc.es/gitlab/dlb/talp-pages/-/raw/main/templates/generate-html/template.yml
    inputs:
      stage: deploy
      generating_job: talp-create-artifacts
      enviroment: production
      dlb_home: ./dlb_talp
      job_name: talp-gen-html
```

## License

Talp-Pages is available under the General Public License v3.0.
