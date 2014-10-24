Summary:	Common CA Certificates
Name:		ca-certificates
Version:	20141019
Release:	1
License:	GPL v2 (scripts), MPL v2 (mozilla certs), distributable (other certs)
Group:		Libraries
Source0:	ftp://ftp.debian.org/debian/pool/main/c/ca-certificates/%{name}_%{version}.tar.xz
# Source0-md5:	f619282081c8bfc65ea64c37fa5285ed
URL:		http://www.cacert.org/
BuildRequires:	openssl-tools
BuildRequires:	openssl-tools-perl
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildArch:	noarch
Requires(post):	findutils
Requires(post):	openssl-tools-perl
Requires(post):	run-parts
Requires:	coreutils
Requires:	openssl-tools
Obsoletes:	ca-certificates-update
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Common CA Certificates.

%prep
%setup -q

%build
%{__make} \
	SUBDIRS=mozilla

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/ca-certificates,%{_sbindir},/etc/{ca-certificates/update.d,ssl/certs}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT	\
	SUBDIRS=mozilla

find $RPM_BUILD_ROOT%{_datadir}/ca-certificates -name '*.crt' -exec sed -i -e 's/\r$//' {} \;

(
cd $RPM_BUILD_ROOT%{_datadir}/ca-certificates
find . -name '*.crt' | sort | cut -b3-
) > $RPM_BUILD_ROOT%{_sysconfdir}/ca-certificates.conf

touch $RPM_BUILD_ROOT/etc/ssl/certs/ca-certificates.crt

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/update-ca-certificates --fresh || :

%files
%defattr(644,root,root,755)
%doc debian/README.Debian debian/changelog
%attr(755,root,root) %{_sbindir}/update-ca-certificates
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ca-certificates.conf
%ghost /etc/ssl/certs/ca-certificates.crt
%dir /etc/ca-certificates
%dir /etc/ca-certificates/update.d
%{_datadir}/ca-certificates

