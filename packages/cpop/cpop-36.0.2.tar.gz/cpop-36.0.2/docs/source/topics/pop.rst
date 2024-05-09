===========================
Plugin Oriented Programming
===========================

Plugin Oriented Programming, or POP, is a new programming paradigm targeting a number of
modern software engineering problems. POP presents a new way of looking at programming,
merging concepts from OOP, Functional, DataFlow, Configuration Management concepts and
more.

POP puts weight on plugins, namespaces, modularity and isolation of development and testing.

The Components of POP
=====================

Everything is a Plugin
----------------------

When developing large codebases it is extremely common to need to move code into a modular
design over time. This typically means that the application needs to be overhauled after
the first few years of development to be modular and pluggable. So why not just start with
a plugin design to begin with?

POP is turtles all the way down. Using the POP design forces you to make your code pluggable.
The unique design allows for all of the code components to be easily replaced so long
as the exposed interfaces remain the same.

When everything is a plugin from the beginning it becomes easy to replace individual
components and compartments of an application. When the application gets split up cleanly
into plugin subsystems then entire plugin subsystems can be replaced or updated
wholesale. When needed, instead of being stuck with code not intended to scale to the
scope a project so often finds itself in.

Global Namespace - The Hub
--------------------------

The first thing you will notice in POP is the ``hub`` object. The hub is passed automatically
as the first argument to all functions, much like ``self`` inside a python class. This hub
can be infinitely extended to include new plugin subsystems as well as namespaces and
variables.

The hub is critical as it serves as a vehicle for accessing all of the plugin subsystems
that are made available to the application.

Plugin Subsystems
-----------------

Plugin Subsystems, which are simply referred to as ``subs`` allow for new plugin systems to be added
to the hub. This makes merging codebases easy. Other applications can be merged together by
including their plugin subsystems. For instance an application can be written that creates
an authentication system, and then the entire structure of that application can then be
added to another application as a subsystem.

Contracts
---------

Plugin systems need to be able to support interfaces. In fact interfaces as a programming
construct become more important than ever. Instead of having the overhead of class inheritance,
contracts can server and transparent interfaces to enforce and guide plugin developers.

Contracts get executed transparently, this allows for a developer to simply implement
the interface without needing to also inherit an Abstract Base Class. Beyond this,
contracts allow for pre and post hooks to be applied to functions in contracted plugins.

This allows for things like interface input validation. Built in pre and post hooks. As
well as load time enforcement of the validity of the interface.

App Merging
-----------

App merging allows for full applications to be merged into each other. This means that
a large application can be developed as many small applications that can be merged together.

Since any single application is comprised of ``subs`` it becomes easy to merge multiple subs
together from multiple apps into a new larger app.

Horizontal App Merging
~~~~~~~~~~~~~~~~~~~~~~

Horizontal app merging means that you take the ``subs`` from multiple applications and merge
them together into a new larger application. For instance lets say that you have a process
that exposes an rpc interface, but you want to add system data gathering to your rpc system.
Just use horizontal app merging to bring in the functionality from another application.
In a nutshell, Horizontal App Merging allows for functionality from multiple apps to
be merged together by adding more ``subs`` onto your `hub`.

Vertical App Merging
~~~~~~~~~~~~~~~~~~~~

Vertical App merging happens when you have a ``sub`` but you want to extend that ``sub`` to
support more plugins that folow your `sub`'s pattern and contracts. This can be
useful when you want to add additional database support, or support interacting with more
Operating Systems. Or when you want to add support for interacting with more apis.

Challenges to Face
==================

POP is designed to address a number of challenges in modern software engineering. These challenges
include, but are not limited to...

Distributed Development
-----------------------

One of the best aspects of modern open source software is the distributed nature of development.
Having many people working on a large, important piece of software is a serious challenge, not
only in co-ordination of development, but also in the maintainability of said software stack.
As many developers come together to push forward a project many problems also occur. Projects
originally designed to be small and lean become bloated and feature laden. Systems that once
could be tested in seconds grow to tests that take hours. Feature creep takes over and the
beautiful concepts of clean software design get swept up in the excitement of a large scale
project.

POP is designed to make software development compartmentalizable. This idea is that entire
functional components of a larger applications can be developed reliably in isolation.
If the functional components of an application can be compartmentalized, that means they
can be tested standalone and then merged back into a greater whole. This takes the main
benefits of a microservices design and applies to to a cleanly ordered application
development model.

Concurrency Models
------------------

Over the last few years new concepts about concurrency have emerged, primarily in the
sense of modern co-routines. Coroutines allow for concurrent processing without threading
but they also impose unique challenges. The POP model presents a way for coroutines to
cross communicate in clean and reliable ways, and allow for coroutines to be run without
the headaches that so often occur using things like callbacks and having multiple
coroutine streams running.

This is accomplished using the `Hub`. The hub in POP allows for clean, globally accessible memory
to be accessed in a safe, namespaced way, while still honoring valuable OOP concepts of
encapsulation, without over encapsulating data that is so often useful in the broader application.
This namespaced approach to development makes data sharing between coroutines safe,
easy and reliable.
