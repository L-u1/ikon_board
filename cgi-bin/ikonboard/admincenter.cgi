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

&testsystem;

use CGI::Carp "fatalsToBrowser";          # Output errors to browser
use CGI qw(:standard);                    # Saves loads of work
$CGI::POST_MAX=1024 * 150;                # limit post data
$CGI::DISABLE_UPLOADS = 1;                # Disable uploads

eval {
($0 =~ m,(.*)/[^/]+,)   and unshift (@INC, "$1");
($0 =~ m,(.*)\\[^\\]+,) and unshift (@INC, "$1");
require "ikon.lib";           # Require ikonboard ()
require "ikonadmin.lib";      # Require Admin func()
require "data/progs.cgi";     # Require prog names
require "data/boardinfo.cgi"; # Require board info
require "data/styles.cgi";    # Require styles info
require "data/boardstats.cgi";# Require styles info
};
if ($@) {
print header('text/html; charset=windows-1251'); print start_html(-title=>"$ibtxt{'0025'}");
    print "$ibtxt{'0026'} $@\n$ibtxt{'0027'}";
    print end_html; exit;
}

#################--- Begin the program ---###################


$thisprog = "admincenter.cgi";

# sort out the incoming CGI

$query = new CGI;

$action       = $query -> param('action');
$inmembername = $query -> param('membername');
$inpassword   = $query -> param('password');
$inmembername = &unHTML("$inmembername");
$inpassword   = &unHTML("$inpassword");

if ($action eq "remove") {
$filetounlink = "$ikondir" . "install.cgi";
unlink "$filetounlink";
} # end action

$filetocheck = "$ikondir" . "install.cgi";
if (-e $filetocheck) {
    print "Content-type: text/html\n\n";
    print qq(
    <HTML><HEAD><TITLE>$ibtxt{'0226'}</TITLE></HEAD>
    <BODY BGCOLOR=#ffffff TEXT=#000000>
    <H1>$ibtxt{'0025'}</H1><FONT COLOR=#ff0000><B>$ibtxt{'0233'}</B>:
    $ibtxt{'0234'}</FONT></body></html>);
    exit;
    }

if ($action eq "login") {
    print "Set-Cookie: adminname=$inmembername\;";
    print "\n";
    print "Set-Cookie: adminpass=$inpassword\;";
    print "\n";
    }
    else {
        $inmembername = cookie('adminname');
        $inpassword   = cookie('adminpass');
        }
        
print header('text/html; charset=windows-1251');
        &admintitle;
           
        &getmember("$inmembername");
        
        
        if (($membercode eq "ad") && ($inpassword eq $password) && ($inmembername eq $membername)) {

                # Check board stats

                $filetoopen = "$ikondir" . "data/allforums.cgi";
                $filetoopen = &stripMETA($filetoopen);
                open(FILE, "$filetoopen");
                @files = <FILE>;
                close(FILE);

                $check = @files;
                $check = "failed" unless ($check > 0);

                $filetoopen = "$ikondir" . "data/allforums.bak";
                $backup_file = "true" if (-e $filetoopen);
                
                $warning = qq~<br><font face=verdana size=3 color=#000000>$ibtxt{'0201'} <b>$ibtxt{'0235'}</b></font>~;

                if (($check eq "failed") && ($backup_file eq "true")) {
                    $warning = qq~<br><font face=verdana size=3 color=#FF0000><b>$ibtxt{'0202'}</b><br><font size=-1> $ibtxt{'0203'} <a href="checkboard.cgi">$ibtxt{'0204'}</a> $ibtxt{'0205'}</font>~;
                    }
                    
                $current_time = localtime;
                $inmembername =~ s/\_/ /g;

                $start_topic_ratio = $totalthreads / $totalmembers if $totalthreads;
                $start_topic_ratio = substr($start_topic_ratio, 0, 4) if $totalthreads;
                $posting_ratio = $totalposts / $totalmembers if $totalposts;
                $posting_ratio = substr($posting_ratio, 0, 4) if $totalposts;

                $testcookie = $ENV{HTTP_COOKIE};

                if ($testcookie) {
                    $cookie_result = qq($ibtxt{'0206'});
                    }
                    else {
                        $cookie_result = qq(<font color=#FF0000>$ibtxt{'0207'}</font>);
                        }

                $cgipath = $ENV{SCRIPT_FILENAME};
                $cgipath =~ s/$thisprog//g;

                $hacklog = "$ikondir" . "data/hacklog.cgi";
                if (-e $hacklog) {
                    $last_hack_entry = (stat("$hacklog"))[9];
                    $longdatehack  = &longdate("$last_hack_entry");
                    $shorttimehack = &shorttime("$last_hack_entry");
                    $last_hack_entry = "$ibtxt{'0211'} $longdatehack, $shorttimehack";
                    }
                    else {
                         $last_hack_entry = "$ibtxt{'0237'}";
                         }   
                
                print qq(
                <tr><td bgcolor=#333333" ><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center>
                <font face=verdana color=#333333 size=3><b>$ibtxt{'0115'} $inmembername</b></font>
                </td></tr>
                <tr><td bgcolor=#FFFFFF>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#000000 size=2>
                <center>
                $ibtxt{'0209'} <b>$current_time</b>
                </center>

                $warning
                
                <hr>
                <font color=#000000 size=2 face=verdana>
                <p>
                <b>$ibtxt{'0210'}</b><br><br>
                $ibtxt{'0238'} = $last_hack_entry
		<br><br>
                $ibtxt{'0020'} $totalmembers
                <br>$ibtxt{'0212'} $totalposts
                <br>$ibtxt{'2916'}: $totalthreads<br>
                <br>$ibtxt{'0214'} $start_topic_ratio
                <br>$ibtxt{'0215'} $posting_ratio
                <br><br>
                <b>$ibtxt{'0216'}</b> <font color=#FF0000>$cgipath</font>
                <br>$ibtxt{'0217'} <font color=#FF0000>$]</font> $ibtxt{'0219'}
                <br>$ibtxt{'0220'} $cookie_result
                <br><hr>
                <b>$ibtxt{'0221'}</b> Matthew Mecham<br>
                <b>$ibtxt{'0222'}</b>Debbie Ruff<br>
                <b>$ibtxt{'0223'}</b>Ken, Luc and Josh
                </font>
                </td></tr></table></td></tr></table>
                );
                
                }
                else {
                    &adminlogin;
                    }
                




print qq~</td></tr></table></body></html>~;
exit;






sub testsystem {

if (1 == 0) {
print "Content-type: text/html\n\n";
print qq(
<HTML><HEAD><TITLE>$ibtxt{'0226'}</TITLE></HEAD>
<BODY BGCOLOR=#ffffff TEXT=#000000>
<H1>$ibtxt{'0025'}</H1>
$ibtxt{'0225'}<p></body></html>
);
exit:
}

$prog = $0;

open (PROG, $prog);
@prog = <PROG>;
close (PROG);
$perl = $prog[0];
$perl =~ s/^#!//;
$perl =~ s/\s+$//;


if ($] < 5.004) {
    
    print "Content-type: text/html\n\n";
    print qq(
    <HTML><HEAD><TITLE>$ibtxt{'0226'}</TITLE></HEAD>
    <BODY BGCOLOR=#ffffff TEXT=#000000>
    <H1>$ibtxt{'0025'}</H1><FONT COLOR=#ff0000><B>$ibtxt{'0227'}</B>:  $ibtxt{'0228'}<B>$perl</B>, $ibtxt{'0229'} $]
    $ibtxt{'0230'}</FONT></body></html>);
exit;  
}






}
