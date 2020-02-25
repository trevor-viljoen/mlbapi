# Contributing to mlbapi

The following guidelines are considered best practice for contributing to the mlbapi project.

#### Table of Contents

* [Code of Conduct](#code-of-conduct)
* [I just have a question](#questions)
* [Contributing](#contributing)
* [Additional Resources](#additional-resources)

## Code of Conduct
### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team on Slack. All complaints will be reviewed
and investigated and will result in a response that is deemed necessary and
appropriate to the circumstances. The project team is obligated to maintain
confidentiality with regard to the reporter of an incident. Further details of
specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/

## Questions
Please don't file an issue to ask a question. The best place for questions is the mlbapi Slack Team.
* Join the mlbapi Slack Team! [![Join Slack](https://img.shields.io/badge/slack-join-blue.svg)](https://pymlbapi-slack-invite.herokuapp.com/)

## Contributing
### Getting Started
* Make sure you have a [GitHub account](https://github.com/signup/free).
* Open an issue via the GitHub issue tracker.
* Fork the repository on GitHub.
* You agree to the
  [LICENSE](https://github.com/trevor-viljoen/mlbapi/blob/master/LICENSE).

### Making Changes
* Create a topic branch from where you want to base your work.
  * This is usually the master branch.
  * Only target release branches if you are certain your fix must be on that branch.
  * To quickly create a topic branch based on master, run `git checkout -b fix/master/my_contribution master`.
    Please avoid working directly on the master branch.
* Make commits of logical and atomic units.
* Check for unnecessary whitespace with `git diff --check` before committing.
* Make sure your commit messages are in the proper format.
```
Add code necessary to Fix #1

This code does the needful by implementing these important changes:
  - Import change fixes foo
  - Another important change, because it does the thing

This message addresses all of the things I did in this commit,
describing them and their relevance to fixing this issue.

```
* Make sure your code follows the [Google Python Style
  Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).
* Make sure you have added the necessary tests for your changes.
* Run all the tests to assure nothing else was accidentally broken.

### Submitting Changes
* Push your changes to a topic branch in your fork of the repository.
* Submit a pull request to the repository.
* Optional: post a link to the pull request in `#general` on slack.
* Changes will be reviewed by the mlbapi team for quality, style, and
  how they address the related issue(s). If approved, they will be
merged and included in a future release.

## Additional Resources
* [General GitHub documentation](https://help.github.com/)
* [GitHub pull request documentation](https://help.github.com/articles/creating-a-pull-request/)
* [mlbapi Slack Team](https://pymlbapi.slack.com)
* [Contributor
  Covenant](https://www.contributor-covenant.org/version/1/4/code-of-conduct.html)
* [License](https://github.com/trevor-viljoen/mlbapi/blob/master/LICENSE)
