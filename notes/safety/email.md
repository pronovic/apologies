# Safety Vulnerability Scanner

## Vulnerability Scanning

Previously, I used the Safety scanner as part of my pre-commit hooks and GitHub actions, to identify vulnerabilities in Python dependencies.  This functionality was removed in [PR #33](https://github.com/pronovic/apologies/pull/33).  Even though Safety is distributed under the liberal [MIT license](license.png), and the PyPI package page [documents that Safety can be used in this manner](usage.png), the PyUp organization behind Safety now claims that this usage is not allowed.  (See the bizarre email thread captured below &mdash; it has some hallmarks of a phishing email, but appears to be legitimate.)  Despite my repeated attempts to clarify what I was doing wrong, PyUp's representative never offered any specifics.

## PyUp Email

```
From: Tristan Laurillard <tristan@pyup.io>
Date: Thu, Nov 25, 2021 at 4:50 PM
Subject: Using Safety in your GitHub projects

Hi Kenneth,

My name is Tristan Laurillard, I work for PyUp.

I see on Github that you are utilizing PyUp Safety in some of your projects.
Although we are always grateful to see that people find our service useful, I
am sorry to inform you of some unfortunate news…

Our free service can not be used for commercial or closed-source purposes. We
are in the process of making various changes to enforce this, and, regrettably,
need to ask you to stop integrating our service with your projects because they
do allow commercial use.

Even if your projects did not allow any commercial use, we still would ask you
to remove the code that queries our database as there are too many commercial
teams that ignore such license limitations.

Would you please write me back once you have removed PyUp Safety from your
projects?

Greetings from Salt Spring Island,

Tristan Laurillard
Operations Manager
PyUp.io

----

From: Kenneth Pronovici
Date: Thu, Nov 25, 2021 at 6:07 PM
Subject: Re: Using Safety in your GitHub projects
To: Tristan Laurillard <tristan@pyup.io>

I don't think I understand. All of my code distributed at github.com/pronovic
is open source, under either GPL v2 (in one case) or Apache 2.0, and all of my
repos are public.  I'm the sole copyright owner in most cases, and certainly
there is no business that has any part in maintaining this code. What
commercial use are you referring to, specifically?

----

From: Tristan Laurillard <tristan@pyup.io>
Date: Fri, Nov 26, 2021 at 12:55 PM
Subject: Re: Using Safety in your GitHub projects
To: <pronovic.com>

Hello,

Even if your code does not allow commercial use, we still do not want others to
pass on our service.

Here is where I looked:
uci-parse / LICENSE
apologies / LICENSE
cedar-backup3 / LICENSE

All three say:

Permissions
✔ Commercial use

Tristan

----

From: Kenneth Pronovici
Date: Fri, Nov 26, 2021 at 2:33 PM
Subject: Re: Using Safety in your GitHub projects
To: Tristan Laurillard <tristan@pyup.io>

Of course those licenses say that commercial use is allowed.  That's the entire
point of an open source license - anyone can use the code regardless of their
field of endeavor.  Any license that does discriminate against a specific field
of endeavor (like making a distinction between commercial vs. non-commercial
use of a Python library) is not open source, by definition.

I use Safety as a build time dependency (to run checks as part of my pre-commit
hooks and in my GitHub action), and it's not used or exposed at all to anything
that uses my code as a dependency or a command line tool.  The only time Safety
would ever be used is if someone clones the repo and tries to run the test
suite, or when they submit a PR and the GitHub action runs.  Technically, the
dependency is referenced (but not used) by readthedocs.io because of the
doc-specific requirements.txt file they need for their build process.  So, I
can't see how I could possibly be passing on your service to others in a legal
sense.  

What, specifically, is wrong with this usage of Safety?

----

From: Tristan Laurillard <tristan@pyup.io>
Date: Fri, Nov 26, 2021 at 3:40 PM
Subject: Re: Using Safety in your GitHub projects

Hi Kenneth,

I too wish there would be the option to look for wiggle room or to discuss the
nuances, but unfortunately there is no way around the policy of our company. We
really must ask you to stop using Safety inside your GitHub code.

We allow the usage of Safety in some scenarios but not in others. The way you
are using Safety is ― I am very sorry ― just not allowed.

Tristan Laurillard
Operations Manager
PyUp.io
```
