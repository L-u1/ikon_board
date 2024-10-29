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
require "$ikondir" . "ikonadmin.lib";     # Require Admin func()
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

$thisprog = "checkboard.cgi";

$query = new CGI;

$inforum       = $query -> param("forum");
$inforum       = &cleaninput("$inforum");
$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");

print header('text/html; charset=windows-1251');

&admintitle;

&getmember("$inmembername");
        
        if (($membercode eq "ad") && ($inpassword eq $password) && ($inmembername eq $membername)) {


        if ($action eq "restoreforums") {

        $filetoopen = "$ikondir" . "data/allforums.bak";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, "$filetoopen");
          flock (FILE, 2);
        @files = <FILE>;
        close(FILE);

        $totalforums = @files;

        $filetomake = "$ikondir" . "data/allforums.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, ">$filetomake") or die "$ibtxt{'0324'}";
          flock (FILE, 2);
        foreach (@files) {
            chomp $_;
            print FILE "$_\n";
            }
        close(FILE);

        print qq~
        <tr><td bgcolor=#333333 colspan=3><font face=verdana size=3 color=#FFFFFF>
        <b>$ibtxt{'0401'}</b>
        </td></tr>
        <tr><td bgcolor=#FFFFFF colspan=3><font face=verdana size=2 color=#333333>
        <b>$ibtxt{'0402'}</b><br><br>
        $ibtxt{'0403'}<br><br>
        $ibtxt{'0404'} $totalforums $ibtxt{'0405'}
        </td></tr>
        ~;
        }


        elsif ($action eq "restorelist") {


            $filetoopen = "$ikondir" . "forum$inforum/list.bak";
            $filetoopen = &stripMETA($filetoopen);
            open(FILE, "$filetoopen");
              flock (FILE, 2);
            @files = <FILE>;
            close(FILE);

            $totaltopics = @files;

            $filetomake = "$ikondir" . "forum$inforum/list.cgi";
            $filetoopen = &stripMETA($filetoopen);
            open(FILE, ">$filetomake") or die "$ibtxt{'0324'}";
              flock (FILE, 2);
            foreach (@files) {
                chomp $_;
                print FILE "$_\n";
                }
            close(FILE);

            print qq~
            <tr><td bgcolor=#333333 colspan=3><font face=verdana size=3 color=#FFFFFF>
            <b>$ibtxt{'0401'}</b>
            </td></tr>
            <tr><td bgcolor=#FFFFFF colspan=3><font face=verdana size=2 color=#333333>
            <b>$ibtxt{'0402'}</b><br><br>
            $ibtxt{'0406'} $inforum list.cgi $ibtxt{'0407'}<br><br>
            $ibtxt{'0407'} $totaltopics $ibtxt{'0408'}
            </td></tr>
            ~;
            }

            else {
           

                $filetoopen = "$ikondir" . "data/allforums.cgi";
                $filetoopen = &stripMETA($filetoopen);
                open(FILE, "$filetoopen");
                  flock (FILE, 2);
                @files = <FILE>;
                close(FILE);

                $check = @files;
                $check = "failed" unless ($check > 0);

                $filetoopen = "$ikondir" . "data/allforums.bak";
                $backup_file = "true" if (-e $filetoopen);
                
                $allforums = qq~$ibtxt{'0411'}</font>~;

                if (($check eq "failed") && ($backup_file eq "true")) {
                    $allforums = qq~<b>$ibtxt{'0409'}</b> - <a href="$thisprog?action=restoreforums">$ibtxt{'0410'}</a>~;
                    }
                    
                if ($backup_file eq "true") {
                    $allforums_backup = qq~$ibtxt{'0412'}~;
                    }
                    else {
                      $allforums_backup = qq~$ibtxt{'0413'}~;
                      }

                
                foreach (@files) { #s
                    chomp($_);
                    ($tempno, $trash) = split(/\|/,$_);
                    $filetoopen = "$ikondir" . "forum$tempno/list.cgi";
                    $filetoopen = &stripMETA($filetoopen);
                    open(FILE, "$filetoopen");
                      flock (FILE, 2);
                    @test = <FILE>;
                    close(FILE);

                    $filetocheck = "$ikondir" . "forum$tempno/list.bak";

                    if (-e $filetocheck) { 
                      $listback_up = "true"; 
                      }


                    $check = @test;
                    $check = "failed" unless ($check > 0);
  
                    if (($check eq "failed") && ($listback_up eq "true")){
                        $result = "Forum $tempno $ibtxt{'0414'} - <a href=\"$thisprog?action=restorelist&forum=$tempno\">$ibtxt{'0415'}</a>";
                        }
                        else {
                           $result = "Forum $tempno $ibtxt{'0416'}";
                           }
                    push (@results, $result);
                    } #e 

                # Print out the results

                print qq~
                <tr><td bgcolor=#333333 colspan=3><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0401'}</b>
                </td></tr>
                <tr><td bgcolor=#FFFFFF colspan=3><font face=verdana size=2 color=#333333>
                <b>$ibtxt{'0417'}</b><br><br>
                $ibtxt{'0418'}<br>
                <font color=#FF0000><b>$ibtxt{'0419'}</b>
                <font face=verdana size=2 color=#333333>  
                <br><br>
                <b>$ibtxt{'0420'} allforums.cgi file:</b> <br><br>$allforums<br><br></font>
                <font face=verdana size=2 color=#333333>
                <b>$ibtxt{'0420'} allforums backup:</b> <br><br>$allforums_backup</font>
                <hr>
                <font face=verdana size=2 color=#333333>
                <br><b>$ibtxt{'0421'} list.cgi $ibtxt{'0422'}</b>
                <br><br>
                ~;

                foreach (@results) {
                    chomp $_;
                    print qq($_<br><br>\n);
                    }
                print qq~
                <br><hr><br><i>$ibtxt{'0423'}</i>
                </td></tr>
                ~;
                } # end if
          

       } # end if admin
       else {
            &adminlogin;
            }


print qq~</table></td></tr></table></td></tr></table></body></html>~;
exit;













