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
require "ikonadmin.lib";     # Require Admin func()
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

$thisprog = "checklog.cgi";

$query = new CGI;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;


$wordarray     = $query -> param('wordarray');
$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");

print header('text/html; charset=windows-1251');

&admintitle;
            
        &getmember("$inmembername");

        die "No such user!" if ($userregistered eq "no");
        
        if (($membercode eq "ad") && ($inpassword eq $password) && ($inmembername eq $membername)) {
                
        if ($action eq "delete") {
                
            $filetotrash = "$ikondir" . "data/hacklog.cgi";
            unlink $filetotrash;

            print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'} / $ibtxt{'5013'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>$ibtxt{'5013'}</b>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=verdana color=#000000 size=2>
                <b>$ibtxt{'5014'}</b>
                </font></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=verdana color=#000000 size=2>
                <br>);

            }
            
            else {

                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'} / $ibtxt{'5013'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>$ibtxt{'5013'}</b>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=verdana color=#000000 size=2>
                $ibtxt{'5015'}
                </font></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=verdana color=#000000 size=2>
                <br>);
    
                $filetoopen = "$ikondir" . "data/hacklog.cgi";

                if (-e $filetoopen) {
                    open (LOG, "$filetoopen");
                    local $/ = undef;
                    $raw_data = <LOG>;
                    close (LOG);

                    @hackdata = split(/\------Log Entry------/,$raw_data);

                    print @hackdata;

                    print qq~<br><br>$ibtxt{'0423'} - <a href="$thisprog?action=delete">$ibtxt{'5016'}</a>~;
                    }
                    else {
                         print "$ibtxt{'5017'}";
                         }
                    
                } # end show log

                }
                else {
                    &adminlogin;
                    }
        
print qq~</td></tr></table></td></tr></table></td></tr></table></body></html>~; 
exit;
