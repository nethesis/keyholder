Name:          keyholder
Version:       1.0.1
Release:       2
URL:           https://phabricator.wikimedia.org/source/keyholder
License:       ASL 2.0
Summary:       ssh agent proxy to securely share one ssh agent and keys.
Provides:      keyholder = %{version}-%{release}
Provides:      config(keyholder) = %{version}-%{release}
Requires:      config(keyholder) = %{version}-%{release}
%{?systemd_requires}
BuildRequires: systemd
Requires(pre): shadow-utils
Requires:      python34 python34-PyYAML
Source0: https://github.com/nethesis/%{name}/archive/rpmbuild.tar.gz
%prep
%autosetup -n %{name}-rpmbuild
%description
keyholder provides a means of allowing a group of trusted
users to use a shared SSH identity without exposing the identity's
private key.

%pre
getent group keyholder >/dev/null || groupadd -r keyholder
getent passwd keyholder >/dev/null || \
    useradd -r -g keyholder -d /dev/null -s /sbin/nologin \
    -c "Keyholder SSH Agent Proxy" keyholder
exit 0

%install
mkdir -p %{buildroot}%{_bindir}
cp -p bin/keyholder %{buildroot}%{_bindir}
cp -p bin/ssh-agent-proxy %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/keyholder.d
mkdir -p %{buildroot}%{_sysconfdir}/keyholder-auth.d
cp -p etc/keyholder.conf %{buildroot}%{_sysconfdir}/keyholder-auth.d
mkdir -p %{buildroot}%{_unitdir}
cp -p etc/systemd/system/keyholder-agent.service %{buildroot}%{_unitdir}
cp -p etc/systemd/system/keyholder-proxy.service %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_mandir}/man1
cp -p docs/keyholder.1 %{buildroot}%{_mandir}/man1
cp -p docs/keyholder-auth.1 %{buildroot}%{_mandir}/man1
cp -p docs/ssh-agent-proxy.1 %{buildroot}%{_mandir}/man1

%files
%dir %attr(0755, keyholder, keyholder) %{_sysconfdir}/keyholder-auth.d
%dir %attr(0750, keyholder, keyholder) %{_sysconfdir}/keyholder.d
%config %attr(0444, keyholder, keyholder) %{_sysconfdir}/keyholder-auth.d/keyholder.conf
%attr(0644, root, root) %{_unitdir}/keyholder-agent.service
%attr(0644, root, root) %{_unitdir}/keyholder-proxy.service
%attr(0755, root, root) %{_bindir}/keyholder
%attr(0755, root, root) %{_bindir}/ssh-agent-proxy
%doc CREDITS LICENSE *.md docs

%{_mandir}/man1/keyholder.1*
%{_mandir}/man1/keyholder-auth.1*
%{_mandir}/man1/ssh-agent-proxy.1*

%post
%systemd_post keyholder-agent.service
%systemd_post keyholder-proxy.service

%preun
%systemd_preun keyholder-proxy.service
%systemd_preun keyholder-agent.service

%postun
%systemd_postun_with_restart keyholder-proxy.service
%systemd_postun_with_restart keyholder-agent.service

%changelog
* Fri Oct 20 2017 Davide Principi <davide.principi@nethesis.it> 1.0.1-2
- Nethesis rebuild

* Fri Sep 22 2017 Matt Vaughn <nethershaw@gmail.com> 1.0.1-1
- Initial RPM release
