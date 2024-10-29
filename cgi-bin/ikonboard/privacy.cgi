#!/usr/bin/perl

#############################################################
# Ikonboard v2.1
# Copyright 2001 Ikonboard.com - All Rights Reserved
# Ikonboard is a trademark of Ikonboard.com
#
# Software Distributed by: Ikonboard.com
# Visit us online at http://www.ikonboard.com
# Email us on boards@ikonboard.com
#
# All files written by Matthew Mecham
#############################################################

use CGI::Carp "fatalsToBrowser";          # Output errors to browser
use CGI qw(:standard);                    # Saves loads of work
$CGI::POST_MAX=1024 * 150;                # limit post data
$CGI::DISABLE_UPLOADS = 1;                # Disable uploads
$CGI::HEADERS_ONCE = 1;                   # Make sure we only have 1 header

eval {
($0 =~ m,(.*)/[^/]+,)   and unshift (@INC, "$1");
($0 =~ m,(.*)\\[^\\]+,) and unshift (@INC, "$1");
require "ikon.lib";          # Require ikonboard ()
require "data/progs.cgi";    # Require prog names
require "data/boardinfo.cgi";# Require board info
require "data/styles.cgi";   # Require styles info
};
if ($@) {
print header('text/html; charset=windows-1251'); print start_html(-title=>"$ibtxt{'0025'}");
    print "$ibtxt{'0026'} $@\n$ibtxt{'0027'}";
    print end_html; exit;
}

$|++;                                    # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "privacy.cgi";


&title;

    $output .= qq~
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
        <tr>
            <td width=30% rowspan=2>
            <img src="$imagesurl/images/$boardlogo" border=0>
            </td>
            <td valign=top align=left>
                <font face="$font" color=$fontcolormisc size=$dfontsize2>
	            &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">&nbsp;&nbsp;$boardname</a>
	            <br>
                &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;$ibtxt{'1701'}
            </td>
            </tr>
            <tr>
        <td valign=bottom align=right>&nbsp; $helpurl</td>
    </tr>
    </table>
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=6 cellspacing=1 border=0 width=100%>
    ~;


    
    $filetoopen = "$ikondir" . "data/privacy.dat";

    open(FILE,$filetoopen) or die "$ibtxt{'1702'}";
    @filedata = <FILE>; close(FILE);
    foreach (@filedata) { $tempoutput .= $_; }
    
    $output .= qq~
    <tr>
    <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc size=$dfontsize3>
    <b>$boardname - $ibtxt{'1701'}</b>
    </td>
    </tr>
    <td bgcolor=$miscbackone align=left><font face="$font" color=$fontcolormisc size=$dfontsize2>
    $tempoutput
    </td>
    </tr>
    </table>
    </td></tr></table>
    ~;

    $output =~ s/\$adminemail_in/$adminemail_in/sg;

print header('text/html; charset=windows-1251');
    
    &output(
    -Title   => $boardname, 
    -ToPrint => $output, 
    -Version => $versionnumber 
    );

