Summary:	Configuration management system
Name:		bcfg2
Version:	1.0.1
Release:	0.1
License:	BSD
Group:		Applications/System
URL:		http://trac.mcs.anl.gov/projects/bcfg2
Source0:	ftp://ftp.mcs.anl.gov/pub/bcfg/%{name}-%{version}.tar.gz
# Source0-md5:	6fbf36acc5cc58b2504a25c25cad3921
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bcfg2 helps system administrators produce a consistent, reproducible,
and verifiable description of their environment, and offers
visualization and reporting tools to aid in day-to-day administrative
tasks. It is the fifth generation of configuration management tools
developed in the Mathematics and Computer Science Division of Argonne
National Laboratory.

It is based on an operational model in which the specification can be
used to validate and optionally change the state of clients, but in a
feature unique to bcfg2 the client's response to the specification can
also be used to assess the completeness of the specification. Using
this feature, bcfg2 provides an objective measure of how good a job an
administrator has done in specifying the configuration of client
systems. Bcfg2 is therefore built to help administrators construct an
accurate, comprehensive specification.

Bcfg2 has been designed from the ground up to support gentle
reconciliation between the specification and current client states. It
is designed to gracefully cope with manual system modifications.

Finally, due to the rapid pace of updates on modern networks, client
systems are constantly changing; if required in your environment,
Bcfg2 can enable the construction of complex change management and
deployment strategies.

%package -n bcfg2-server
Summary:	Bcfg2 Server
Group:		Networking/Daemons
Requires:	bcfg2
Requires:	pydoc
Requires:	python-lxml
Requires:	python-pyOpenSSL

%description -n bcfg2-server
Bcfg2 helps system administrators produce a consistent, reproducible,
and verifiable description of their environment, and offers
visualization and reporting tools to aid in day-to-day administrative
tasks. It is the fifth generation of configuration management tools
developed in the Mathematics and Computer Science Division of Argonne
National Laboratory.

It is based on an operational model in which the specification can be
used to validate and optionally change the state of clients, but in a
feature unique to bcfg2 the client's response to the specification can
also be used to assess the completeness of the specification. Using
this feature, bcfg2 provides an objective measure of how good a job an
administrator has done in specifying the configuration of client
systems. Bcfg2 is therefore built to help administrators construct an
accurate, comprehensive specification.

Bcfg2 has been designed from the ground up to support gentle
reconciliation between the specification and current client states. It
is designed to gracefully cope with manual system modifications.

Finally, due to the rapid pace of updates on modern networks, client
systems are constantly changing; if required in your environment,
Bcfg2 can enable the construction of complex change management and
deployment strategies.

%prep
%setup -q

%build
export CFLAGS="%{rpmcflags}"
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
        --optimize=2 \
        --root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_initrddir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/default
install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly
install -d $RPM_BUILD_ROOT%{_libdir}/bcfg2
%{__mv} $RPM_BUILD_ROOT%{_bindir}/bcfg2* $RPM_BUILD_ROOT%{_sbindir}
install redhat/scripts/bcfg2.init $RPM_BUILD_ROOT/etc/rc.d/init.d/bcfg2
install redhat/scripts/bcfg2-server.init $RPM_BUILD_ROOT/etc/rc.d/init.d/bcfg2-server
install debian/bcfg2.default $RPM_BUILD_ROOT%{_sysconfdir}/default/bcfg2
install debian/bcfg2-server.default $RPM_BUILD_ROOT%{_sysconfdir}/default/bcfg2-server
install debian/bcfg2.cron.daily $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/bcfg2
install debian/bcfg2.cron.hourly $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/bcfg2
install tools/bcfg2-cron $RPM_BUILD_ROOT%{_libdir}/bcfg2/bcfg2-cron

%clean
rm -rf $RPM_BUILD_ROOT

%post -n bcfg2-server
/sbin/chkconfig --add bcfg2-server

%files -n bcfg2
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/bcfg2
%dir %{py_sitescriptdir}/Bcfg2
%{py_sitescriptdir}/Bcfg2/*.py[co]
%dir %{py_sitescriptdir}/Bcfg2/Client
%{py_sitescriptdir}/Bcfg2/Client/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_initrddir}/bcfg2
%config(noreplace) %{_sysconfdir}/default/bcfg2
%{_sysconfdir}/cron.hourly/bcfg2
/etc/cron.daily/bcfg2
%{_libdir}/bcfg2/bcfg2-cron

%files -n bcfg2-server
%defattr(644,root,root,755)
%attr(754,root,root)  /etc/rc.d/init.d/bcfg2-server
%{py_sitescriptdir}/Bcfg2/Server
%{_datadir}/bcfg2
%config(noreplace) %{_sysconfdir}/default/bcfg2-server
%attr(755,root,root) %{_sbindir}/bcfg2-admin
%attr(755,root,root) %{_sbindir}/bcfg2-build-reports
%attr(755,root,root) %{_sbindir}/bcfg2-info
%attr(755,root,root) %{_sbindir}/bcfg2-ping-sweep
%attr(755,root,root) %{_sbindir}/bcfg2-repo-validate
%attr(755,root,root) %{_sbindir}/bcfg2-reports
%attr(755,root,root) %{_sbindir}/bcfg2-server
%{_mandir}/man8/*.8*
%dir %{_libdir}/bcfg2
