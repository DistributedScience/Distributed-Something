This folder contains the files to automatically generate documentation for your Distributed-Something distribution using [Jupyter Book](https://jupyterbook.org/en/stable/intro.html) using GitHub Actions.
Read more about [GitHub Actions](https://help.github.com/en/actions) and about [hosting Jupyter Books with GitHub Actions](https://jupyterbook.org/en/stable/publish/gh-pages.html#automatically-host-your-book-with-github-actions).
This documentation is linked from the main repository README and serves in place of a wiki.

Instructions for customizing your Distributed-Something distribution are in the `Creating DS` section and can be deleted from your repository's documentation you have completed creating your Distributed-Something distribution.

Documentation for running Distributed-Something are in the `Running DS` section and should be updated to fit your particular Distributed-Something implementation.

To enable this auto-build, you need to set up two GitHub Actions in your repository:

The first action is automatically set up by the deploy.yml configuration file in .github/workflows.
It will auto-build the documentation to a `gh-pages` branch.
This documentation will automatically re-build any time you push edits in the documentation files to your repository's `main` branch.
By default, only pages that have undergone edits will rebuild.
You only need to edit your [deploy.yml](.github/workflows/deploy.yml) if you change path names of documentation/DS-documentation.

The second action deploys the `gh-pages` branch to a Jupyterbook visible at `yourorganization.github.io/yourrepository`.
To create this action, on GitHub, navigate to Settings => Pages.
Select `Build and deployment`: `Source`: `Deploy from a branch`.
Select `Branch`: `gh-pages/root`
