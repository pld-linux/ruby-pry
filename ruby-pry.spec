#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	pry
Summary:	An IRB alternative and runtime developer console
Name:		ruby-%{pkgname}
Version:	0.9.12
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	-
URL:		http://pry.github.com
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-bacon < 2
BuildRequires:	ruby-bacon >= 1.2
BuildRequires:	ruby-bond < 0.5
BuildRequires:	ruby-bond >= 0.4.2
BuildRequires:	ruby-guard < 1.4
BuildRequires:	ruby-guard >= 1.3.2
BuildRequires:	ruby-mocha < 0.14
BuildRequires:	ruby-mocha >= 0.13.1
BuildRequires:	ruby-open4 < 2
BuildRequires:	ruby-open4 >= 1.3
BuildRequires:	ruby-rake < 1
BuildRequires:	ruby-rake >= 0.9
%endif
Requires:	ruby-coderay < 1.1
Requires:	ruby-coderay >= 1.0.5
Requires:	ruby-method_source < 1
Requires:	ruby-method_source >= 0.8
Requires:	ruby-slop < 4
Requires:	ruby-slop >= 3.4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An IRB alternative and runtime developer console

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{pkgname}-%{version}
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%build
# write .gemspec
%__gem_helper spec

%if %{with tests}
bacon -Ispec -q spec/*_spec.rb
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir},%{_bindir},%{_mandir}/man1}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a man/pry.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.markdown LICENSE CHANGELOG CONTRIBUTORS
%attr(755,root,root) %{_bindir}/pry
%{_mandir}/man1/pry.1*
%{ruby_vendorlibdir}/pry.rb
%{ruby_vendorlibdir}/pry
%{ruby_specdir}/pry-%{version}.gemspec
