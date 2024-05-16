# Updating Your Distributed-Something Implementation

We expect to continue to improve Distributed-Something and it is possible that a developer will want to implement some of the changes that occur to the DS codebase after they have created their implementation from the template.
Unlike forks, for which Github currently provides a "sync fork" function, templates do not have an automatic way of pulling changes from the template into repositories made from the template.
These six lines of [code described here](https://stackoverflow.com/questions/56577184/github-pull-changes-from-a-template-repository/69563752#69563752) simply explain how to pull template changes into your repository.  

Because Distributed-Something is so customizable, we expect that implementations will diverge from the template.
Developers should feel free to take what is useful for their application but otherwise change the framework as radically as they need to.
Therefore, not all developers will want to incorporate code changes made after using the template, nor would all downstream changes even be functional or relevant in all implementations.

If you anticipate wanting to keep your implementation more closely linked to the DS template, you can fork the template to create your own project repository instead and use the "sync fork" function as necessary.
