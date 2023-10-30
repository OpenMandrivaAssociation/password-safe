%define sname pwsafe

Summary:	A cross-platform password database utility
Name:		password-safe
Version:	1.18.0
Release:	1
License:	Artistic
Group:		File tools
URL:		https://pwsafe.org/
Source0:	https://github.com/pwsafe/%{sname}/archive/refs/tags/%{version}/%{sname}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	gtest-devel
BuildRequires:	imagemagick
BuildRequires:	libyubikey-devel
BuildRequires:	wxgtku3.0-devel
BuildRequires:	zip
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libmagic)
BuildRequires:	pkgconfig(libqrencode)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(xerces-c)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(ykpers-1)

Requires:	xvkbd

%description
Password Safe is a password database utility. Like many other such
products, commercial and otherwise, it stores your passwords in an
encrypted file, allowing you to remember only one password (the "safe
combination"), instead of all the username/password combinations that
you use.

%files -f %{name}.lang
%license docs/LICENSE.rtf
%doc README.md
#doc docs/help
%doc docs/pwsafe-state-machine.rtf
%doc docs/ChangeLog.txt
%doc docs/config.txt
%doc docs/formatV1.txt
%doc docs/formatV2.txt
%doc docs/formatV3.txt
%doc docs/formatV4.txt
%doc docs/help.txt
%doc docs/ReleaseNotes.md
%doc docs/*.html
%{_bindir}/%{sname}
%{_bindir}/%{sname}-cli
%{_datadir}/%{sname}/
%{_datadir}/applications/%{sname}.desktop
%{_datadir}/pixmaps/%{sname}.xpm
%{_iconsdir}/hicolor/*/apps/%{sname}.png
%{_docdir}/%{sname}/help/
%{_mandir}/man1/%{sname}.1*

%prep
%autosetup -p1 -n %{sname}-%{version}

# fix path
sed -i -e '{
		s,/usr/share/passwordsafe/help/,%{_docdir}/%{sname}/help/,
		s,/usr/share/passwordsafe/xml/,%{_datadir}/%{sname}/xml/,
	    }' src/os/unix/dir.cpp

sed -i -e '{
		s,share/doc/passwordsafe,share/doc/%{sname},
		s,share/pwsafe,share/%{sname},
		s,share/passwordsafe,share/%{sname},
		}' CMakeLists.txt

%build
%cmake \
	-DXML_XERCESC:BOOL=ON \
	-DNO_YUBI:BOOL=OFF \
	-DNO_GTEST:BOOL=OFF \
	-DGTEST_BUILD:BOOL=OFF \
	-DNO_QR:BOOL=OFF \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# icons
for d in 16 32 48 64 72 128 256
do
	install -dm 755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none install/graphics/%{sname}.png \
		-scale ${d}x${d} %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{sname}.png
done
install -dm 755 %{buildroot}%{_datadir}/pixmaps/
convert -background none install/graphics/%{sname}.png \
	-scale 32x32 %{buildroot}%{_datadir}/pixmaps/%{sname}.xpm

# localizations
%find_lang %{name} --all-name

# help
install -dm 0755 %{buildroot}%{_docdir}/%{sname}/help/
install -pm 0644 build/help/help*zip %{buildroot}%{_docdir}/%{sname}/help/

# we are not Debian
rm -fr %{buildroot}%{_docdir}/%{sname}/{changelog.Debian,copyright}

%check
# desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/%{sname}.desktop

