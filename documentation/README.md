This folder contains the files to automatically generate documentation for your Distributed-Something distribution using [Jupyter Book](https://jupyterbook.org/en/stable/intro.html).
This documentation is linked from the main repository README and serves in place of a wiki.

Instructions for customizing your Distributed-Something distribution are in the `Creating DS` section and can be deleted from your repository's documentation you have completed creating your Distributed-Something distribution.

Documentation for running Distributed-Something are in the `Running DS` section and should be updated to fit your particular Distributed-Something implementation.

This documentation will automatically re-build any time you push to your repository's `main` branch.
By default, only pages that have undergone edits will rebuild.

To enable this auto-build, you need to set up a GitHub Action in your repository.
Read more about [GitHub Actions](https://help.github.com/en/actions) and about [hosting Jupyter Books with GitHub Actions](https://jupyterbook.org/en/stable/publish/gh-pages.html#automatically-host-your-book-with-github-actions).
It will auto-build the documentation to a `gh-pages` branch which will be visible at `githubusername.github.io/yourbookname`.
