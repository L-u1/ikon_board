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

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "whosonline.cgi";


if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie");   }

if ($inmembername eq "") {
    $inmembername = "$ibtxt{'0043'}";
    }
    else {
        &getmemberstime("$inmembername");
        }

$helpurl = &helpfiles("Пользователи_в_On-line");
$helpurl = qq~$helpurl<img src="$imagesurl/images/help_b.gif" border=0></a>~;

&title;

$output .= qq~
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
    <tr>
        <td width=30% rowspan=2><img src="$imagesurl/images/$boardlogo" border=0></td>
        <td valign=middle align=left><font face="$font" color=$fontcolormisc size=$dfontsize2>
            &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">&nbsp;&nbsp;$boardname</a>
	        <br>
            &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;$ibtxt{'0113'}
        </td>
        <tr>
        <td valign=bottom align=right>&nbsp; $helpurl</td>
    </tr>
</table>
<p>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>
        <td>
        <table cellpadding=6 cellspacing=1 border=0 width=100%>
        <tr>
        <td bgcolor=$miscbacktwo valign=middle colspan=3 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'0113'}</b></font>
    </td>
</tr>
~;

    $filetoopen = "$ikondir" . "data/onlinedata.dat";
    open(FILE,"$filetoopen");
    @onlinedata = <FILE>;
    close(FILE);

    $output .= qq~
        <tr>
        <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'2501'}</b></font></td>
        <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'2502'}</b></font></td>
        <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'2503'}</b></font></td>
    </tr>
    ~;
            
foreach $line (@onlinedata) {
    chomp $line;
    ($savedusername, $savedtime, $savedwhere) = split(/\|/, $line);
    $savedtime = $savedtime + ($timezone*3600) + ($timedifferencevalue*3600);
    $longdate = &longdate("$savedtime");
    $shorttime = &shorttime("$savedtime");
    $savedtime = "$longdate - $shorttime";
    $lookfor = substr($savedusername, 0, 5);
    if ($lookfor eq "$ibtxt{'0043'}") { $savedusername = "$ibtxt{'0043'}"; }
    if ($savedusername eq "$ibtxt{'0043'}" && $savedwhere eq "Logging in") { next; }
    
    $output .=qq~
    <tr>
    <td bgcolor=$miscbackone nowrap><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$savedusername</b></font></td>
    <td bgcolor=$miscbackone nowrap><font face="$font" color=$fontcolormisc size=$dfontsize2>$savedtime</font></td>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1>$savedwhere</font></td>
    </tr> ~;
    }
    
$output .= qq~</table></td></tr></table>~;

print header('text/html; charset=windows-1251');
&output(
       -Title   => "$boardname - $ibtxt{'0113'}", 
       -ToPrint => $output, 
       -Version => $versionnumber 
       );
