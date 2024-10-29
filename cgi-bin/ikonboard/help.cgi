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
require "$ikondir" . "ikon.lib";          # Require ikonboard ()
require "$ikondir" . "data/progs.cgi";    # Require prog names
require "$ikondir" . "data/boardinfo.cgi";# Require board info
require "$ikondir" . "data/styles.cgi";   # Require styles info
};
if ($@) {
print header('text/html; charset=windows-1251'); print start_html(-title=>"$ibtxt{'0025'}");
    print "$ibtxt{'0026'} $@\n$ibtxt{'0027'}";
    print end_html; exit;
}

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "help.cgi";

$query = new CGI;
	
$inadmin                = $query -> param('admin');
$action                 = $query -> param('action');
$inhelpon               = $query -> param('helpon');
$inadminmodpass         = $query -> param("adminmodpass");
$inadminmodname         = $query -> param("adminmodname");

$inadminmodpass         = &cleaninput($inadminmodpass);
$inadminmodname         = &cleaninput($inadminmodname);
$inhelpon               = &cleaninput($inhelpon);
$inhelpon =~ s/\///g;
$inhelpon =~ s/\.\.//g;
$cleanhelpname = $inhelpon;
$cleanhelpname =~ s/\_/ /g;

$cleanadminname = $inadmin;
$cleanadminname =~ s/\_/ /g;

if (($number) && ($number !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = cookie("apasswordcookie"); }


if ($inmembername eq "" || $inmembername eq "$ibtxt{'0043'}") {
    $inmembername = "$ibtxt{'0043'}";
    }
    else {
        &getmemberstime("$inmembername");
        }

print header('text/html; charset=windows-1251');

    if ($inhelpon) {

        ### Print Header for the page.

        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
                <tr>
                <td>
                    <table cellpadding=3 cellspacing=1 border=0 width=100%>
                        <tr>
                            <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc size=3><b>$boardname $ibtxt{'0123'}</b></td>
                        </tr>
                        <tr>
                            <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc size=$dfontsize2>
                            <br><center>$ibtxt{'0115'} $inmembername, $ibtxt{'0703'}.</center><br>
                            <font face="$font" color=$fontcolormisc size=1>
                            <b>$ibtxt{'0704'} $cleanhelpname</b><p>
                            ~;

    
        ### Grab the help file
    
        $filetoopen = "$ikondir" . "help/$inhelpon.dat";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen") or die "$ibtxt{'0326'}";
        @helpdata = <FILE>;
        close (FILE);
    
        #Display the helpfile
    
        foreach (@helpdata) {
            $output .= $_;
            }
            
            
        } # end if.
        
        
        
        
        
        
        
        
        elsif ($action eq "login") {
        
            &getmember("$inadminmodname");
            
            unless ($membercode eq "ad" || $membercode eq "mo") { &messengererror("$ibtxt{'0123'}&$ibtxt{'0705'}."); }
            if ($inadminmodpass ne $password) { &messengererror("$ibtxt{'0123'}&$ibtxt{'0303'}."); }
     
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
                <tr>
                <td>
                    <table cellpadding=3 cellspacing=1 border=0 width=100%>
                        <tr>
                            <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$boardname $ibtxt{'0707'}</b></td>
                        </tr>
                        <tr>
                            <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc size=$dfontsize2>
                            <br><center>$ibtxt{'0115'} $inadminmodname, $ibtxt{'0708'}.</center><br>
                            <font face="$font" color=$fontcolormisc size=$dfontsize1>
                            <b>$ibtxt{'0713'}</b><p>
                            ~;
            
            
            
            
            
            
            $dirtoopen = "$ikondir" . "help";
            opendir (DIR, "$dirtoopen") or die "$ibtxt{'0709'} $dirtoopen"; 
            @dirdata = readdir(DIR);
            closedir (DIR);

            @sorteddirdata = grep(/cgi/,@dirdata);
            @newdirdata = sort alphabetically(@sorteddirdata);
            
            foreach (@newdirdata) {
                chomp $_;
                $filename = $_;
                $filename =~ s/\.cgi//g;
                
                $cleanname = $filename;
                $cleanname =~ s/\_/ /g;
                
                $output .= qq~$ibtxt{'0704'} <a href="$thisprog?admin=$filename" target="_self"><b>$cleanname</b></a><p>~;
                }
            
            
            
            } # end action
        
        
        
        
        
        
        elsif ($inadmin) {

        &getmember("$inmembername");
            
        unless ($membercode eq "ad" || $membercode eq "mo") { &messengererror("$ibtxt{'0123'}&$ibtxt{'0705'}."); }
        if ($inpassword ne $password) { &messengererror("$ibtxt{'0123'}&$ibtxt{'0303'}."); }
        
        
        ### Print Header for the page.

        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
                <tr>
                <td>
                    <table cellpadding=3 cellspacing=1 border=0 width=100%>
                        <tr>
                            <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$boardname $ibtxt{'0707'}</b></td>
                        </tr>
                        <tr>
                            <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc size=$dfontsize2>
                            <br><center>$ibtxt{'0115'} $inmembername, $ibtxt{'0703'}.</center><br>
                            <font face="$font" color=$fontcolormisc size=$dfontsize1>
                            <b>$ibtxt{'0704'} $cleanadminname</b><p>
                            ~;

    
        ### Grab the help file
    
        $filetoopen = "$ikondir" . "help/$inadmin.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen") or die "$ibtxt{'0326'}";
        @helpdata = <FILE>;
        close (FILE);
    
        #Display the helpfile
    
        foreach (@helpdata) {
            $output .= $_;
            }
            
            
        } # end if.
        
        
        
        
        
        
        
        
        
        
        else {
            
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
                <tr>
                <td>
                    <table cellpadding=3 cellspacing=1 border=0 width=100%>
                        <tr>
                            <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$boardname $ibtxt{'0123'}</b></td>
                        </tr>
                        <tr>
                            <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc size=$dfontsize2>
                            <br><center>$ibtxt{'0702'} $inmembername, $ibtxt{'0708'}.</center><br>
                            <font face="$font" color=$fontcolormisc size=$dfontsize1>
                            <b>$ibtxt{'0713'}</b><p>
                            ~;
            
            $dirtoopen = "$ikondir" . "help";
            opendir (DIR, "$dirtoopen"); 
            @dirdata = readdir(DIR);
            closedir (DIR);

            @sorteddirdata = grep(/dat/,@dirdata);
            @newdirdata = sort alphabetically(@sorteddirdata);
            
            foreach (@newdirdata) {
                chomp $_;
                $filename = $_;
                $filename =~ s/\.dat//g;
                
                $cleanname = $filename;
                $cleanname =~ s/\_/ /g;
                
                $output .= qq~$ibtxt{'0704'} <a href="$thisprog?helpon=$filename" target="_self"><b>$cleanname</b></a><p>~;
                }
    
    
        } #end else
    
    
    
    





    ## Print the footer, and the page.  
    
    if ($passwordverification eq "yes") { $passwordverification = "$ibtxt{'0714'}"; }
    else { $passwordverification = "$ibtxt{'0715'}"; }
    
    if ($emailfunctions ne "on") { $emailfunctions = "off"; }
    
    if ($emoticons eq "on") {
                $emoticons = "$ibtxt{'0716'}";
                $emoticonslink = qq~| $ibtxt{'0719'} <a href="javascript:openwin('$miscprog?action=showsmilies',300,350)">$ibtxt{'0717'}</a>~;
                }
                else { $emoticons = "$ibtxt{'0718'}"; }
            
            
    $output .= qq~<p><br><br>$ibtxt{'0719'} <a href="$thisprog" target="_self">$ibtxt{'0720'}</a> $emoticonslink | $ibtxt{'0719'} <a href="javascript:openwin('$miscprog?action=ikoncode',300,350)">$ibtxt{'0721'}</a>~;
        
    ## All done, print the file
    
    $output .= qq~
    </td></tr>
    <tr>
    <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'0722'}</b><br>
    <font size=$dfontsize1>$ibtxt{'0723'} <b>$emoticons</b><br>$ibtxt{'0724'} $passwordverification<br>$ibtxt{'0725'} <b>$emailfunctions</b>
    </td>
    </tr>
    <tr>
    <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0726'}.</b><br>
    
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="login">
    <font face="$font" color=$fontcolormisc size=$dfontsize1>
    $ibtxt{'0727'} &nbsp; <input type=text name="adminmodname" value="$inmembername" size=15> &nbsp; 
    $ibtxt{'0728'} &nbsp; <input type=password name="adminmodpass" value="$inpassword" size=15> &nbsp; <input type=submit value="$ibtxt{'0040'}"></td></tr></form>
    </table></td></tr></table>~;
    
            &printmessenger(
            -Title   => "$boardname - $ibtxt{'0114'}", 
            -ToPrint => $output, 
            -Version => $versionnumber 
            );
    
    
sub messengererror {

my $errorinfo = shift;

($where, $errormsg) = split(/\&/, $errorinfo);

$output = qq~
<table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
    <tr>    
        <td>
        <table cellpadding=6 cellspacing=1 border=0 width=100%>
        <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'0120'} $where</b></font></td></tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize2>
                <b>$ibtxt{'0121'} $where $ibtxt{'0729'}</b>
                <ul>
                <li><b>$errormsg</b>
                <li>$ibtxt{'0122'} <a href="$helpprog">$ibtxt{'0123'}</a>?
                </ul>
                <b>$ibtxt{'0124'} $where $ibtxt{'0120'}</b>
                <ul>
                <li>$ibtxt{'0125'}
                <li>$ibtxt{'0126'}
                <li><a href="$registerprog">$ibtxt{'0127'}</a> $ibtxt{'0136'}
                </ul>
                </tr>
                </td></tr>
                <tr>
                <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2> <a href="javascript:history.go(-1)"> << $ibtxt{'0128'}</a>
                </td></tr>
                </table></td></tr></table>
                ~;
            &printmessenger(
            -Title   => $boardname, 
            -ToPrint => $output, 
            -Version => $versionnumber 
            );
}
   


