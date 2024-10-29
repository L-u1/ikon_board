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

$thisprog = "setmembers.cgi";

$query = new CGI;

&checkVALIDITY;

$action          = $query -> param('action');
$checkaction     = $query -> param('checkaction');
$inletter        = $query -> param('letter');
$inmember        = $query -> param('member');
$inmember        = &unHTML("$inmember");
$action          = &unHTML("$action");

$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");


print header('text/html; charset=windows-1251');     
&admintitle;
        
&getmember("$inmembername");
        
        
        if (($membercode eq "ad") && ($inpassword eq $password) && ($inmembername eq $membername)) {
            
            print qq~
            <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
            <b>$ibtxt{'0208'} / $ibtxt{'0811'}</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'updatecount'        =>    \&docount,
            'viewletter'         =>    \&viewletter,
            'edit'               =>    \&edit,        
            'deletemember'       =>    \&deletemember,
            'unban'              =>    \&unban
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
               }
                else { &memberoptions; }
            
            print qq~</table></td></tr></table>~;
            }
                
            else {
               &adminlogin;
               }
        

##################################################################################
######## Subroutes (forum list)


sub memberoptions {

    $dirtoopen = "$ikondir" . "members";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @sortedfile = sort(@filedata);
    @sortedfile = grep(/cgi/,@sortedfile);

    foreach (@sortedfile) {
        $fr = substr($_, 0, 1);
        $fr =~ tr/a-z/A-Z/;
        push(@letters,$fr);
        }

    @sortedletters = sort(@letters);

     
    print qq~
     
    <tr>
    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
    <font face=verdana color=#990000 size=3><b>$ibtxt{'2201'}</b>
    </td>
    </tr>          
                
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <font face=verdana color=#333333 size=2><b><a href="$thisprog?action=updatecount">$ibtxt{'2202'}</a></b><br>
    $ibtxt{'2203'}
    </td>
    </tr>         
                
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <font face=verdana color=#333333 size=2><b>$ibtxt{'2204'}</b><br>
    $ibtxt{'2205'}<p>
    ~;
    
    foreach (@sortedletters) {
        unless ($_ eq "$ltr") {
            $tempoutput .= qq~<a href="$thisprog?action=viewletter&letter=$_">&nbsp;$_&nbsp;</a>~;
            $ltr = "$_";
            }
        }
    
    print qq~
    $ibtxt{'2206'}<p>$tempoutput
    </td>
    </tr>           
                
                
                
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <font face=verdana color=#333333 size=2>
    <b>$ibtxt{'2902'}</b><p>
    $ibtxt{'2207'}<br>
    $ibtxt{'2208'}<br><br>
    $ibtxt{'2209'}
    </td>
    </tr>             
     ~;        
     
     } # end routne
     
     
##################################################################################
######## Subroutes (Do member count)  


sub docount {

    $dirtoopen = "$ikondir" . "members";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @countvar = grep(/cgi/,@filedata);
    
    $newtotalmembers = @countvar;
    
        require "$ikondir" . "data/boardstats.cgi";
        
        $filetomake = "$ikondir" . "data/boardstats.cgi";
        
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
        print FILE "\$totalmembers = \"$newtotalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);
    
        print qq~
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <font face=verdana color=#990000 size=3>
                    
        <b>$ibtxt{'2230'}</b><p>
                    
        <font size=-1 color=#333333> $ibtxt{'0404'} $newtotalmembers $ibtxt{'2211'}</font>
                    
        </td></tr>
         ~;
         
     } # end routine

##################################################################################
######## Subroutes (Do member count) 


sub viewletter {

    $dirtoopen = "$ikondir" . "members";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @sortedfile = sort(@filedata);
    @sortedfile = grep(/cgi/,@sortedfile);
    @sortedfile = sort alphabetically(@sortedfile);
    
    foreach (@sortedfile) {
        $fr = substr($_, 0, 1);
        $fr =~ tr/a-z/A-Z/;
        push(@letters,$fr);
        }
    @sortedletters = sort(@letters);
        
    foreach (@sortedletters) {
        unless ($_ eq "$ltr") {
            $tempoutput .= qq~<a href="$thisprog?action=viewletter&letter=$_">&nbsp;$_&nbsp;</a>~;
            $ltr = "$_";
            }
        }

     
    print qq~
    <tr>
    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
    <font face=verdana color=#990000 size=3><b>$ibtxt{'2212'} $inletter</b><p>
    $ibtxt{'2213'} $tempoutput
    </td>
    </tr>          
    ~;
               
               
    foreach (@sortedfile) {
        $ftr = substr($_, 0, 1);
        $ftr =~ tr/a-z/A-Z/;
        if ($inletter eq "$ftr") {
            $_ =~ s/\.cgi//;
            $member = $_;
            &getmember("$member");
            &showmember;
            }
        }
        
   } # end route



##################################################################################
######## Subroutes (Show member) 


sub showmember {

    $joineddate = &longdate("$joineddate");
    
    $cleanmember = $member;
    $cleanmember =~ s/\_/ /g;
    
    ## Sort last post, and where
    
    ($postdate, $posturl, $posttopic) = split(/\%%%/,$lastpostdate);
    
    if ($postdate ne "$ibtxt{'1816'}") {
        $postdate = &longdate("$postdate");
        $lastpostdetails = qq~$ibtxt{'1815'} <a href="$posturl">$posttopic</a> $ibtxt{'1119'} $postdate~;
        }
        else {
            $lastpostdetails = "$ibtxt{'1816'}";
            }

    if ($membercode eq "banned") {
        $unbanlink = qq~ | <a href="$thisprog?action=unban&member=$member">[ $ibtxt{'2231'} ]</a>~;
        }
    
    print qq~
    <tr>
    <td bgcolor=#EEEEEE valign=middle colspan=2 align=center><font face=$font color=$fontcolormisc size=2><b>$ibtxt{'1817'} <font color=$fonthighlight>$cleanmember</b>- <a href="$thisprog?action=edit&member=$member">[ $ibtxt{'2951'} ]</a> | <a href="$thisprog?action=deletemember&member=$member">[ $ibtxt{'2214'} ]</a>$unbanlink</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle width=30%><font face=verdana color=#333333 size=1><b>$ibtxt{'1818'}</b></font></td>
    <td bgcolor=#FFFFFF valign=middle><font face=verdana color=#333333 size=1>$joineddate</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle><font face=verdana color=#333333 size=1><b>$ibtxt{'1819'}</b></font></td>
    <td bgcolor=#FFFFFF valign=middle><font face=verdana color=#333333 size=1>$membertitle</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle><font face=verdana color=#333333 size=1><b>$ibtxt{'2215'}</b></font></td>
    <td bgcolor=#FFFFFF valign=middle><font face=verdana color=#333333 size=1>$lastpostdetails</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle><font face=verdana color=#333333 size=1><b>$ibtxt{'1818'}</b></font></td>
    <td bgcolor=#FFFFFF valign=middle><font face=verdana color=#333333 size=1>$joineddate</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle><font face=verdana color=#333333 size=1><b>$ibtxt{'0212'}</b></font></td>
    <td bgcolor=#FFFFFF valign=middle><font face=verdana color=#333333 size=1>$numberofposts</font></td></tr>
    
    ~;
    $unbanlink = "";
    } # end routine


##################################################################################
######## Subroutes (Edit member) 


sub edit {

    if ($checkaction eq "yes") {
    
    
    $innewpassword      = $query -> param('password');
    $inmembertitle      = $query -> param('membertitle');
    $inemailaddress     = $query -> param('emailaddress');
    $inhomepage         = $query -> param('homepage');
    $inaolname          = $query -> param('aolname');
    $inicqnumber        = $query -> param('icqnumber');
    $inlocation         = $query -> param('location');
    $innumberofposts    = $query -> param('numberofposts');
    $intimedifference   = $query -> param('timedifference');
    $inmembercode       = $query -> param('membercode');

    $inlocation = &cleaninput("$inlocation");
    
    
    if ($inpassword eq "")     { $blank = "yes"; }
    if ($inemailaddress eq "") { $blank = "yes"; }
    
    if ($blank eq "yes") {
    
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2><font face=verdana color=#333333 size=2><b>$ibtxt{'2216'}</b></font></td></tr>
        ~;
        
        }
    

        # Sort out the private access
    
        
        $filetoopen = "$ikondir" . "data/allforums.cgi";
        open(FILE,"$filetoopen");
          flock(FILE,2);
        @forums = <FILE>;
        close(FILE);
        
        foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $trash) = split(/\|/,$forum);
            $namekey = "allow" . "$forumid";
            $tocheck = $query -> param("$namekey");
            if ($tocheck eq "yes") {
                $allowedforums2 .= "$forumid=$tocheck&";
                }
            }
            
        &getmember("$inmember");
    
        $memberfiletitle = $inmember;
        $memberfiletitle =~ s/ /\_/isg;

        

        # Add to ban lists (if required)

        if ($inmembercode eq "banned") { 
            
            $filetoopen = "$ikondir" . "data/banlist.cgi";
            open(FILE,">>$filetoopen");
            print FILE "$inmember|$inemailaddress|$ipaddress\n";
            close(FILE);

            $banresult = "$membername $ibtxt{'2217'}";
            }




        $filetomake = "$ikondir" . "members/$memberfiletitle.cgi";
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "$membername|$innewpassword|$inmembertitle|$inmembercode|$innumberofposts|$inemailaddress|$showemail|$ipaddress|$inhomepage|$inaolname|$inicqnumber|$inlocation|$interests|$joineddate|$lastpostdate|$signature|$intimedifference|$allowedforums2|$useravatar|$misc1|$misc2|$misc3";
        close(FILE);

                print qq~
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>$ibtxt{'2102'}</b><br><br>$banresult<br>
                </td></tr>
                ~;
    
    }
    
    else {
    
    
    
    $filetoopen = "$ikondir" . "data/allforums.cgi";
         open(FILE,"$filetoopen");
           flock(FILE,2);
         @forums = <FILE>;
         close(FILE);

         
         foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);   
            if ($privateforum eq "yes") { 
                $grab = "$forumid|$forumname";
                push(@newforums, $grab);
                }
            }
        $cleanmember = $inmember;
        $cleanmember =~ s/\_/ /g;
    
        &getmember("$inmember");
        
        if($privateforums) {
            @private = split(/&/,$privateforums);
            foreach $accessallowed (@private) {
                chomp $accessallowed;
                ($access, $value) = split(/=/,$accessallowed);
                $allowedentry2{$access} = $value;
                }
            }
    
        @allowedforums = sort alphabetically(@newforums);
        foreach $line (@allowedforums) {
            ($forumid, $forumname) = split(/\|/,$line);
            if ($allowedentry2{$forumid} eq "yes") { $checked = " checked"; }
            else { $checked = ""; }
            $privateoutput .= qq~<input type="checkbox" name="allow$forumid" value="yes"$checked>$forumname<br>\n~;
            }
            
    $memberstateoutput = qq~<select name="membercode"><option value="me">$ibtxt{'0136'}<option value="banned">$ibtxt{'2218'}<option value="ad">$ibtxt{'1874'}<option value="mo">$ibtxt{'0007'}</select>~;
    
    $memberstateoutput =~ s/value=\"$membercode\"/value=\"$membercode\" selected/g;
    
    print qq~
    <form action="$thisprog" method=post>
    <input type=hidden name="action" value="edit">
    <input type=hidden name="checkaction" value="yes">
    <input type=hidden name="member" value="$inmember">
    <tr>
    <td bgcolor=#EEEEEE colspan=2><font face=verdana color=#333333 size=3><b>$ibtxt{'2219'}</b>$membername</td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=verdana color=#333333 size=1><b>$ibtxt{'1819'}</b><br>$ibtxt{'2220'}</td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="membertitle" value="$membertitle"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=verdana color=#333333 size=1><b>$ibtxt{'2221'}</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="numberofposts" value="$numberofposts"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=verdana color=#333333 size=1><b>$ibtxt{'0728'}</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="password" value="$password"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=verdana color=#333333 size=1><b>$ibtxt{'1822'}</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="emailaddress" value="$emailaddress"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font face=verdana color=#333333 size=1><b>$ibtxt{'1823'}</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="homepage" value="$homepage"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font face=verdana color=#333333 size=1><b>$ibtxt{'1841'}</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="aolname" value="$aolname"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font face=verdana color=#333333 size=1><b>$ibtxt{'1825'}</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="icqnumber" value="$icqnumber"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font face=verdana color=#333333 size=1><b>$ibtxt{'1826'}</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="location" value="$location"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font face=verdana color=#333333 size=1><b>$ibtxt{'1845'}</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="timedifference" value="$timedifference"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF align=left colspan=2><font face=verdana color=#333333 size=1><b>$ibtxt{'2222'}</b><br>
    $privateoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font face=verdana color=#333333 size=1><b>$ibtxt{'2223'}</b></td>
    <td bgcolor=#FFFFFF>$memberstateoutput</td>
    </tr><tr>
    <td colspan=2 bgcolor=#EEEEEE align=center><input type=submit value=$ibtxt{'0039'} name=submit></form></td>
    </tr>
    ~;
    
    } # end else
    
} # endroute


############### delete member

sub deletemember {

if ($checkaction eq "yes") {

    # Check to see if they were the last member to register

    require "$ikondir" . "data/boardstats.cgi";
        

    if($inmember eq "$lastregisteredmember") { #start
        
        # If they were, go through the members, and find the previous last registered

        $dirtoopen = "$ikondir" . "members";

        opendir (DIR, "$dirtoopen"); 
        @filedata = readdir(DIR);
        closedir (DIR);
        @inmembers = grep(/cgi/,@filedata);

        local($highest) = 0;

        foreach (@inmembers) {
            $_ =~ s/\.cgi//g;
            &getmember("$_");
            if (($joineddate > $highest) && ($inmember ne $membername)) {
                $highest = $joineddate;
                $memberkeep = $membername;
                }
        }
        


        $filetomake = "$ikondir" . "data/boardstats.cgi";
        $totalmembers--;
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "\$lastregisteredmember = \"$memberkeep\"\;\n";
        print FILE "\$totalmembers = \"$totalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);
        } # end if new/delete member

    else {
        require "$ikondir" . "data/boardstats.cgi";

        $filetomake = "$ikondir" . "data/boardstats.cgi";
        $totalmembers--;
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
        print FILE "\$totalmembers = \"$totalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);
        } # end if else

        # Delete the database for the member

        $filetounlink = "$ikondir" . "members/$inmember.cgi";
        unlink $filetounlink;

        print qq~
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=verdana color=#333333 size=3><b>$ibtxt{'2224'}</b>
        </td></tr>
         ~;


} # end checkaction else

else {

        $cleanedmember = $inmember;
        $cleanedmember =~ s/\_/ /g;

        print qq~
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=verdana color=#990000 size=3><b>$ibtxt{'1884'}</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <font face=verdana color=#333333 size=2>$ibtxt{'2225'} <b>$cleanedmember</b><p>
        &raquo;<a href="$thisprog?action=deletemember&checkaction=yes&member=$inmember">$ibtxt{'2226'}</a>&laquo;
        </td></tr>
        </table></td></tr></table>
        ~;
        }

} # end routine


sub unban {

        &getmember("$inmember");
    
        $memberfiletitle = $inmember;
        $memberfiletitle =~ s/ /\_/isg;

        # Remove from ban lists
            
        $filetoopen = "$ikondir" . "data/banlist.cgi";
        open(FILE,"$filetoopen");
        @bandata = <FILE>;
        close(FILE);

        open(FILE,">$filetoopen");
          flock (FILE, 2);
        foreach (@bandata) {
            chomp $_;
            ($bannedname, $bannedemail, $bannedip) = split(/\|/,$_);
            $bannedname =~ s/\_/ /g;
            unless ($bannedname eq $membername) { print FILE "$_\n"; }
            }
        close(FILE);
            

        $filetomake = "$ikondir" . "members/$memberfiletitle.cgi";
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "$membername|$password|Member|me|$numberofposts|$emailaddress|$showemail|$ipaddress|$homepage|$aolname|$icqnumber|$location|$interests|$joineddate|$lastpostdate|$signature|$timedifference|$allowedforums|$useravatar|$misc1|$misc2|$misc3";
        close(FILE);

        print qq~
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=verdana color=#333333 size=3><b>$membername $ibtxt{'2227'}</b>
        </td></tr>
        ~;

} # end route


print qq~</td></tr></table></body></html>~;
exit;


 


