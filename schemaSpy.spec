%define _buildid .0

# Upstream doesn't seem to be doing regular releases. :-( 
# So we're going to use the date as the version, and a GIT hash as the
# release. Generate new GIT snapshots using the folowing commands:
#
# $ hash=`git log -1 --format='%h'`
# $ date=`date '+%Y%m%d'`
# $ git archive --output schemaSpy-${date}-git${hash}.tar.gz --prefix schemaSpy-${date}-git${hash}/ ${hash}
#
# And then change these two:

%global date 20150429
%global hash b1521aa

Name:    schemaSpy
Version: %{date}
Release: 1.git%{hash}%{?_buildid}%{?dist}
Summary: Tool for analyzing and graphing database schemas

Group:   Development/Libraries
License: LGPLv2
URL:     http://schemaspy.sourceforge.net/ 

Source0: %{name}-%{version}-git%{hash}.tar.gz
Source1: %{name}.1

BuildRequires: ant >= 1.8.3
BuildRequires: jpackage-utils

Requires: java
Requires: jpackage-utils
Requires: graphviz
Requires: graphviz-gd

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# Lambda Linux patches
Patch1001: 1001-Update-path-to-HSQLDB-driver.patch
Patch1002: 1002-Update-path-to-MySQL-driver.patch
Patch1003: 1003-Update-path-to-Oracle-driver.patch
Patch1004: 1004-Update-path-to-PostgreSQL-driver.patch
Patch1005: 1005-Update-path-to-H2-driver.patch
Patch1006: 1006-Add-PostgreSQL-specific-selectRowCountSql.patch
Patch1007: 1007-Disable-logo-for-improved-security.patch

%description
For package support, please visit
https://github.com/lambda-linux-pkgs/%{name}/issues

schemaSpy is a Java-based tool that analyzes the metadata of a
schema in a database and generates a visual representation of it in a
browser-displayable format. It lets you click through the hierarchy of
database tables via child and parent table relationships as represented
by both HTML links and entity-relationship diagrams. It's also designed
to help resolve the obtuse errors that a database sometimes gives related
to failures due to constraints.

schemaSpy uses JDBC's database metadata extraction services to gather the
majority of its information, but has to make vendor-specific SQL queries
to gather some information such as the SQL associated with a view and
the details of check constraints. The differences between vendors have
been isolated to configuration files and are extremely limited. Almost
all of the vendor-specific SQL is optional.

%prep
%setup -q -n %{name}-%{version}-git%{hash}

# Apply Lambda Linux patches
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1
%patch1007 -p1

%build
%ant rebuild

%install
rm -rf %{buildroot}

# JAR file
install -d %{buildroot}%{_javadir}
install -D -m 0644 target/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
pushd %{buildroot}%{_javadir}
ln -s %{name}-%{version}.jar %{name}.jar
popd

# Command line script
%jpackage_script net.sourceforge.schemaspy.Main "" "" %{name} %{name}

# Man page
install -d %{buildroot}%{_mandir}/man1
install -D -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_javadir}/*
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
