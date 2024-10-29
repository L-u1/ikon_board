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
# This file co-written with ArmandoG
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

$thisprog = "setforums.cgi";

$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");


    $query = new CGI;

    &checkVALIDITY;
    
	@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        $theparam = &cleaninput("$theparam");
		$PARAM{$param} = $theparam;
	    }

    $cookiepath = $query->url(-absolute=>1);
    $cookiepath =~ s/$thisprog//sg;

    $action      =  $PARAM{'action'};
    $inforum     =  $PARAM{'forum'};
    $incategory  =  $PARAM{'category'};
    $checkaction =  $PARAM{'checkaction'};

    $new_categoryname     = $PARAM{'categoryname'};
    $new_categorynumber   = $PARAM{'categorynumber'};
    $new_forumname        = $PARAM{'forumname'};
    $new_forumdescription = $PARAM{'forumdescription'};
    $new_forummoderator   = $PARAM{'forummoderator'};
    $new_htmlstate        = $PARAM{'htmlstate'};
    $new_idmbcodestate    = $PARAM{'idmbcodestate'};
    $new_privateforum     = $PARAM{'privateforum'};
    $new_startnewthreads  = $PARAM{'startnewthreads'};
    $new_forumgraphic     = $PARAM{'forumgraphic'};
   


print header('text/html; charset=windows-1251');

&admintitle;
        
&getmember("$inmembername");
        
        if (($membercode eq "ad") && ($inpassword eq $password) && ($inmembername eq $membername)) { #s1
            
            my %Mode = ( 
            'addforum'            =>    \&addforum,
            'processnew'          =>    \&createforum,
            'edit'                =>    \&editform,
            'doedit'              =>    \&doedit,       
            'addcategory'         =>    \&catform,
            'doaddcategory'       =>    \&doaddcategory,
            'editcatname'         =>    \&editcatname,
            'reordercategories'   =>    \&reordercats,
            'recount'             =>    \&recount
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
               }
                elsif (($action eq "delete") && ($checkaction ne "yes")) { &warning; }
                elsif (($action eq "delete") && ($checkaction eq "yes")) { &deleteforum; }
                else { &forumlist; }
            
            } #e1
                
                else {
                    &adminlogin;
                    }
        

##################################################################################
######## Subroutes (forum list)

sub forumlist {
    $highest = 0;
    print qq~
    <tr><td bgcolor=#333333 colspan=3><font face=verdana size=3 color=#FFFFFF>
    <b>$ibtxt{'0208'} / $ibtxt{'2901'}</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font face=verdana size=1 color=#333333>
    <b>$ibtxt{'2902'}</b><br><br>
    $ibtxt{'2903'}
    </td></tr>
    ~;

    $filetoopen = "$ikondir" . "data/allforums.cgi";
    open(FILE, "$filetoopen");
    @forums = <FILE>;
    close(FILE);

    foreach $forum (@forums) { #start foreach @forums
        chomp $forum;
        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
        $rearrange = ("$categoryplace|$category|$forumname|$forumdescription|$forumid|$threads|$posts");
        push (@rearrangedforums, $rearrange);

    } # end foreach (@forums)

    @finalsortedforums = sort(@rearrangedforums);

    foreach $sortedforums (@finalsortedforums) { #start foreach @finalsortedforums

        ($categoryplace, $category, $forumname, $forumdescription, $forumid, $threads, $posts) = split(/\|/,$sortedforums);
    
        if ($categoryplace ne $lastcategoryplace) { #start if $categoryplace
            print qq~
            <tr>
            <td bgcolor=#EEEEEE width=20% nowrap><font face=verdana color=#333333 size=3>
            <b>&raquo; $category</b><td bgcolor=#EEEEEE width=15% align=center nowrap><font face=verdana color=#333333 size=2><a href="$thisprog?action=editcatname&category=$categoryplace">$ibtxt{'2904'}</a></td><td bgcolor=#EEEEEE width=25% align=left><font face=verdana color=#333333 size=2><a href="$thisprog?action=addforum&category=$categoryplace"><b>$ibtxt{'2905'}</b></a></font></td>
            </td></tr>
            <tr>
            <td bgcolor=#FFFFFF colspan=3 align=left nowrap><font face=verdana color=#333333 size=3>
            <b>$forumname</b><br><font face=verdana color=#333333 size=2>$ibtxt{'2910'} <b>$posts</b> | $ibtxt{'2906'}: <b>$threads</b><br><br><a href="$thisprog?action=edit&forum=$forumid">$ibtxt{'2907'}</a> | <font face=verdana color=#333333 size=2><a href="$thisprog?action=delete&forum=$forumid">$ibtxt{'2908'}</a> | <a href="$thisprog?action=recount&forum=$forumid">$ibtxt{'2909'}</a></font></td>
             </font></td></tr>
            ~;
            } # end if
            else {
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=3 align=left nowrap><hr noshade size=1><font face=verdana color=#333333 size=3>
                <b>$forumname</b><br><font face=verdana color=#333333 size=2>$ibtxt{'2910'} <b>$posts</b> | $ibtxt{'2906'}: <b>$threads</b><br><br><a href="$thisprog?action=edit&forum=$forumid">$ibtxt{'2907'}</a> | <font face=verdana color=#333333 size=2><a href="$thisprog?action=delete&forum=$forumid">$ibtxt{'2908'}</a> | <a href="$thisprog?action=recount&forum=$forumid">$ibtxt{'2909'}</a></font></td>
                </font></td></tr>
                ~;
                }
            $lastcategoryplace = $categoryplace;
            if ($categoryplace > $highest) { $highest = $categoryplace; }
            } # end foreach
    
        $highest++;
        
        print qq~
        <tr>
        <td bgcolor=#EEEEEE colspan=3 align=center><font face=verdana color=#333333 size=3>
        <a href="$thisprog?action=reordercategories"><b>$ibtxt{'2912'}</b></a>
         - <a href="$thisprog?action=addcategory&category=$highest"><b>$ibtxt{'2911'}</b></a>
        </font></td>
        </tr>
        </tr></table></td></tr></table>~;
    
} # end routine.

##################################################################################
######## Recount forum posts


sub recount { #start

        
        $dirtoopen = "$ikondir" . "forum$inforum";
        
        opendir (DIR, "$dirtoopen"); 
        @dirdata = readdir(DIR);
        closedir (DIR);
        
        @thd = grep(/thd/,@dirdata);
        $topiccount = @thd;
        

        foreach $topic (@thd) {
        
        $filetoopen = "$ikondir" . "forum$inforum/$topic";

            open (FILE, "$filetoopen");
            @threads = <FILE>;
            close (FILE);

            $newthreads = @threads;
            $newthreads--;
            $threadcount = ($threadcount + $newthreads);
         }
       
         $threadcount = "0" if (!$threadcount);
         $topiccount  = "0" if (!$topiccount);
                    
        
         $filetoopen = "$ikondir" . "data/allforums.cgi";
         open(FILE,"$filetoopen") or &systemerror("$ibtxt{'2913'} $filetoopen");
         @allforums = <FILE>;
         close(FILE);

         $filetomake = "$ikondir" . "data/allforums.cgi";
         $filetomake = &stripMETA($filetomake);
         foreach $forum (@allforums) { #start foreach @forums
         chomp($forum);
            ($tempno, $trash) = split(/\|/,$forum);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
                    $posts = $threadcount;
                    $threads = $topiccount;
                    $processed_data .= "$forumid|$category|$categoryplace|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastposter|$lastposttime|$threads|$posts|$forumgraphic\n";
                }
            else { $processed_data .= "$forum\n"; }
         }
         if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
         open(FILE, ">$filetomake");
           flock(FILE, 2);
         print FILE $processed_data;
         close(FILE);
         undef $processed_data;
    
         rebuildLIST(-Forum=>"$inforum");

         print qq~
         <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
         <b>$ibtxt{'0208'} / $ibtxt{'2945'}</b>
         </td></tr>
         <tr>
         <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
         <font face=verdana color=#990000 size=3>
         <center><b>$ibtxt{'2915'}</b></center><p>
         $topiccount $ibtxt{'2916'}<p>
         $threadcount $ibtxt{'2917'}
         </td></tr></table></td></tr></table>
         ~;


} # routine ends

##################################################################################
######## Subroutes ( Add forum Form )


sub addforum {

        print qq~
        <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
        <b>$ibtxt{'0208'} / $ibtxt{'2918'}</b>
        </td></tr>
        ~;

        $filetoopen = "$ikondir" . "data/allforums.cgi";
        open(FILE, "$filetoopen");
        @forums = <FILE>;
        close(FILE);


# Find the category name from the number

        foreach (@forums) {
            ($trash, $tempcategoryname, $tempcategoryplace, $trash) = split(/\|/, $_);
            if ($incategory eq $tempcategoryplace) {
                $category = $tempcategoryname;
                }
            }
        
        
# Present the form to be filled in


        print qq~
        
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=verdana color=#990000 size=3><b$ibtxt{'2919'} '$category' $ibtxt{'2920'}</b>
        </td></tr>
                
        <form action="$thisprog" method="post">
        <input type=hidden name="categorynumber" value="$incategory">
        <input type=hidden name="categoryname" value="$category">
        <input type=hidden name="action" value="processnew">       
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2921'}</b><br>$ibtxt{'2922'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumname" value="$forumname"></td>
        </tr>       
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2923'}</b><br>$ibtxt{'2924'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>   
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2925'}</b><br>$ibtxt{'2926'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forummoderator" value="$forummoderator"></td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2927'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <select name="htmlstate">
        <option value="on">$ibtxt{'2616'}<option value="off" selected>$ibtxt{'2615'}</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2928'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <select name="idmbcodestate">
        <option value="on" selected>$ibtxt{'2616'}<option value="off">$ibtxt{'2615'}</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2929'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <select name="privateforum">
        <option value="yes">$ibtxt{'2930'}<option value="no" selected>$ibtxt{'2931'}</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2932'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <select name="startnewthreads">
        <option value="yes" selected>$ibtxt{'2934'}<option value="no">$ibtxt{'2933'}</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2935'}</b><br>$ibtxt{'2936'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumgraphic" value="logo.gif"></td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <input type=submit value=$ibtxt{'0039'} ></form></td></tr></table></td></tr></table>
        ~;
        
} # end route   


##################################################################################
######## Subroutes ( Create Forum )


sub createforum {   


                $filetoopen = "$ikondir" . "data/allforums.cgi";
                open(FILE, "$filetoopen");
                @forums = <FILE>;
                close(FILE);

                # Create a new number for the new forum folder, and files.

                foreach (@forums) {
                    ($forumid, $binit) = split(/\|/,$_);
                    if ($forumid > $high) { $high = $forumid; }
                    }
                    
                $high++;
                
                $newforumid = $high;    

               
                # Lets create the directory.
                
                $dirtomake = "$ikondir" . "forum$newforumid";

                mkdir ("$dirtomake", 0755);
                
                # Lets add a file to stop snoops, and to use to see if the forum was created
                
                $filetomake = "$dirtomake/index.html";
                open(FILE,">$filetomake");
                print FILE "-";
                close(FILE);

                $filetomake = "$dirtomake/.htaccess";
                open(FILE, ">$filetomake");
                  flock (FILE, 2);
                print FILE "AuthUserFile /dev/null\n";
                print FILE "AuthGroupFile /dev/null\n";
                print FILE "AuthName DenyViaWeb\n";
                print FILE "AuthType Basic\n";
                print FILE "\n\n\n\n";
                print FILE "<Limit GET>\n";
                print FILE "order allow,deny\n";
                print FILE "deny from all\n";
                print FILE "</Limit>\n";
                close (FILE);

                $filetoopen = "$ikondir" . "data/allforums.cgi";
                open(FILE, "$filetoopen");
                @forums = <FILE>;
                close(FILE);
   
                foreach $line (@forums) {
                    chomp $line;
                    $processed_data .= "$line\n";
                    }
                $processed_data .= "$newforumid|$new_categoryname|$new_categorynumber|$new_forumname|$new_forumdescription|$new_forummoderator|$new_htmlstate|$new_idmbcodestate|$new_privateforum|$new_startnewthreads|||0|0|$new_forumgraphic";
                if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
                open(FILE, ">$filetoopen");
                  flock(FILE, 2);
                print FILE $processed_data;
                close(FILE);
                undef $processed_data;
                
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'} / $ibtxt{'2937'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                <font face=verdana color=#333333 size=2>
                ~;

                print "<b>Status</b><p>\n";
                print "<ul>\n";
                if (-e $dirtomake) {
                print "<li><b>$ibtxt{'2938'}</b><p>\n";
                    }
                    else {
                        print "<li><b>$ibtxt{'2939'}<p>\n";
                        }
                

                $filetoopen = "$dirtomake/index.html";
                if (-e $filetoopen) {
                    print "<li><b>$ibtxt{'2940'} (index.html) $ibtxt{'2941'}</b><p>\n";
                    }
                    else {
                        print "<li><b>$ibtxt{'2940'} (index.html) $ibtxt{'2942'}</b><p>$ibtxt{'2943'}\n";
                        }
                print "$filetoopen<p>\n";
                print "</ul></td></tr></table></td></tr></table>\n";

} ######## end routine
        
##################################################################################
######## Subroutes ( Warning of Delete Forum )  

sub warning { #start

        print qq~
        <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
        <b>$ibtxt{'0208'} / $ibtxt{'2944'}</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=verdana color=#990000 size=3><b>$ibtxt{'1884'}</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <font face=verdana color=#333333 size=2>$ibtxt{'2946'}<p>
        &raquo;<a href="$thisprog?action=delete&checkaction=yes&forum=$inforum">$ibtxt{'2947'}</a>&laquo;
        </td></tr>
        </table></td></tr></table>
        
        ~;
        
} # end routine     
        
##################################################################################
######## Subroutes ( Deletion of a Forum )  

sub deleteforum { #start

        
        $dirtoopen = "$ikondir" . "forum$inforum";
        
        opendir (DIR, "$dirtoopen"); 
        @dirdata = readdir(DIR);
        closedir (DIR);
        
        @thd = grep(/thd/,@dirdata);
        $thdcount = @thd;
        
        @mal = grep(/mal/,@dirdata);
        @list = grep(/cgi/,@dirdata);


        foreach $topic (@thd) {
        
        $filetoopen = "$ikondir" . "forum$inforum/$topic";

            open (FILE, "$filetoopen");
            @threads = <FILE>;
            close (FILE);

            $newthreads = @threads;

            $threadcount = ($threadcount + $newthreads);

            }
       
            $threadcount--;
                    
        foreach $file (@thd) {
            $filetoremove = "$dirtoopen/$file";
            unlink $filetoremove;
            }
        foreach $file (@mal) {
            $filetoremove = "$dirtoopen/$file";
            unlink $filetoremove;
            }
        foreach $file (@list) {
            $filetoremove = "$dirtoopen/$file";
            unlink $filetoremove;
            }
        
        # Remove all remaining files.

        foreach $file (@dirdata) {
            $filetoremove = "$dirtoopen/$file";
            unlink $filetoremove;
            }

         $dirtoremove = "$ikondir" . "forum$inforum";
         rmdir $dirtoremove;

         $filetoopen = "$ikondir" . "data/allforums.cgi";
         open(FILE,"$filetoopen") or &systemerror("$ibtxt{'2913'} $filetoopen");
           flock (FILE, 2);
         @forums = <FILE>;
         close(FILE);

        foreach $forum (@forums) {
         chomp $forum;
            ($forumid,$category,$notneeded,$notneeded) = split(/\|/,$forum);
                unless ($forumid eq "$inforum") {
                    $processed_data .= "$forum\n";
                    }
                }
         if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
         open(FILE,">$filetoopen");
           flock(FILE,2);
         print FILE $processed_data;
         close(FILE);
         undef $processed_data;

        require "$ikondir" . "data/boardstats.cgi";
        
        $filetomake = "$ikondir" . "data/boardstats.cgi";
        
        $totalthreads = $totalthreads - $thdcount;
        if ( $threadcount == -1) { $threadcount = 0 } 
        $totalposts = $totalposts - $threadcount;
        
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
        print FILE "\$totalmembers = \"$totalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);

                    
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                    <b>$ibtxt{'0208'} / $ibtxt{'2914'}</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                    <font face=verdana color=#990000 size=3>
                    
                    <center><b>$ibtxt{'2914'}</b></center><p>
                    
                    $thdcount $ibtxt{'2949'}<p>

                    $threadcount $ibtxt{'2950'}
                    
                    </td></tr></table></td></tr></table>
                    ~;


} # routine ends

##################################################################################
######## Subroutes ( Editing of a Forum )   

sub editform {

        
        # Grab the line to edit.
        
        $filetoopen = "$ikondir" . "data/allforums.cgi";
         open(FILE,"$filetoopen") or &systemerror("$ibtxt{'2913'} $filetoopen");
           flock(FILE,2);
         @forums = <FILE>;
         close(FILE);

         
         foreach $forum (@forums) {
         chomp $forum;
            ($forumid,$category,$notneeded,$notneeded) = split(/\|/,$forum);
                if ($forumid eq "$inforum") {
                    ($forumid, $categoryname, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);   
                    }
                }
         
# Present the form to be filled in


        print qq~
        <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
        <b>$ibtxt{'0208'} / $ibtxt{'2977'}</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=verdana color=#990000 size=3><b>$ibtxt{'2951'} '$forumname' $ibtxt{'2952'} '$category' $ibtxt{'2920'}</b>
        </td></tr>
                
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="doedit">
        <input type=hidden name="forum" value="$inforum">
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2921'}</b><br>$ibtxt{'2922'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumname" value="$forumname"></td>
        </tr>       
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2923'}</b><br>$ibtxt{'2953'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>   
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2925'}</b><br>$ibtxt{'2926'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forummoderator" value="$forummoderator"></td>
        </tr>
        ~;
        
        $tempoutput = qq~<select name="htmlstate"><option value="on">$ibtxt{'2616'}<option value="off">$ibtxt{'2615'}</select>~;
        $tempoutput =~ s/value=\"$htmlstate\"/value=\"$htmlstate\" selected/g;
        
        print qq~
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2927'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        $tempoutput
        </td>
        </tr>
        ~;
        
        $tempoutput = qq~<select name="idmbcodestate"><option value="on">$ibtxt{'2616'}<option value="off">$ibtxt{'2615'}</select>~;
        $tempoutput =~ s/value=\"$idmbcodestate\"/value=\"$idmbcodestate\" selected/g;
        
        print qq~
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2928'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        $tempoutput
        </td>
        </tr>
        ~;
        
        $tempoutput = qq~<select name="privateforum"><option value="yes">$ibtxt{'2930'}<option value="no">$ibtxt{'2931'}</select>~;
        $tempoutput =~ s/value=\"$privateforum\"/value=\"$privateforum\" selected/g;
        if (!$privateforum) { 
            $tempoutput = qq~<select name="privateforum"><option value="yes">$ibtxt{'2930'}<option value="no" selected>$ibtxt{'2931'}</select>~;
            }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2929'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        $tempoutput
        </td>
        </tr>
        ~;
        
        $tempoutput = qq~<select name="startnewthreads"><option value="yes">$ibtxt{'2934'}<option value="no">$ibtxt{'2933'}</select>~;
        $tempoutput =~ s/value=\"$startnewthreads\"/value=\"$startnewthreads\" selected/g;
        
        print qq~
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2932'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        $tempoutput
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2935'}</b><br>$ibtxt{'2954'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumgraphic" value="$forumgraphic"></td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <input type=submit value=$ibtxt{'0039'} ></form></td></tr></table></td></tr></table>
        ~;
        
} # end route   

##################################################################################
######## Subroutes ( Processing the edit of a forum)    


sub doedit {
        
        # Grab the line to edit.
        
         $filetoopen = "$ikondir" . "data/allforums.cgi";
         open(FILE,"$filetoopen") or &systemerror("$ibtxt{'2913'} $filetoopen");
           flock(FILE,2);
         @forums = <FILE>;
         close(FILE);

         foreach $forum (@forums) {
         chomp $forum;
            ($forumid, $notneeded) = split(/\|/,$forum);
                if ($forumid eq "$inforum") {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);   
                    }
                }

                # Time to process the forms

                $editedline = "$inforum|$category|$categoryplace|$new_forumname|$new_forumdescription|$new_forummoderator|$new_htmlstate|$new_idmbcodestate|$new_privateforum|$new_startnewthreads|$lastposter|$lastposttime|$threads|$posts|$new_forumgraphic";
                chomp $editedline;

                # Lets re-open the file
                
                foreach $forum (@forums) {
                chomp $forum;
                ($tempforumid,$notneeded) = split(/\|/,$forum);
                    if ($tempforumid eq "$inforum") {
                        $processed_data .= "$editedline\n";
                        }
                        else {
                            $processed_data .= "$forum\n";
                            }
                    }
                if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
                $filetoopen = "$ikondir" . "data/allforums.cgi";
                open(FILE,">$filetoopen") or &systemerror("Cannot locate $filetoopen");
                  flock(FILE,2);
                print FILE $processed_data;
                close (FILE);
                undef $processed_data;

                 print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'} / $ibtxt{'2955'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>$ibtxt{'2102'}</b><p>
                <font size=2>
                $ibtxt{'2956'}.</font>
                </td></tr></table></td></tr></table>
                ~;
                
            } # end routine

##################################################################################
######## Subroutes ( Add category/forum Form )


sub catform {

# Present the form to be filled in


        print qq~
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="doaddcategory">
        <input type=hidden name="category" value="$incategory">
        <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
        <b>$ibtxt{'0208'} / $ibtxt{'2911'}</b>
        </td></tr>
        <tr>
        
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=verdana color=#990000 size=3><b>$ibtxt{'2958'}</b>
        </td></tr>
                
                
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2959'}</b><br>$ibtxt{'2960'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="categoryname" value="$categoryname"></td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2921'}</b><br>$ibtxt{'2922'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumname" value="$forumname"></td>
        </tr>       
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2923'}</b><br>$ibtxt{'2924'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>   
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2925'}</b><br>$ibtxt{'2926'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forummoderator" value="$forummoderator"></td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2927'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <select name="htmlstate">
        <option value="on">$ibtxt{'2616'}<option value="off" selected>$ibtxt{'2615'}</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2928'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <select name="idmbcodestate">
        <option value="on" selected>$ibtxt{'2616'}<option value="off">$ibtxt{'2615'}</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2929'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <select name="privateforum">
        <option value="yes">$ibtxt{'2930'}<option value="no" selected>$ibtxt{'2931'}</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2932'}</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <select name="startnewthreads">
        <option value="yes" selected>$ibtxt{'2934'}<option value="no">$ibtxt{'2933'}</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=verdana color=#333333 size=1><b>$ibtxt{'2935'}</b><br>$ibtxt{'2961'}</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumgraphic" value="logo.gif"></td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <input type=submit value=$ibtxt{'0039'} ></form></td></tr></table></td></tr></table>
        ~;
        
} # end route   


##################################################################################
######## Subroutes ( Create New cat/forum )


sub doaddcategory { 

                $filetoopen = "$ikondir" . "data/allforums.cgi";
                open(FILE, "$filetoopen");
                @forums = <FILE>;
                close(FILE);

                # Create a new number for the new forum folder, and files.

                foreach (@forums) {
                    ($forumid, $binit) = split(/\|/,$_);
                    if ($forumid > $high) { $high = $forumid; }
                    }
                    
                $high++;
                
                $newforumid = $high;    

               
                # Lets create the directory.
                
                $dirtomake = "$ikondir" . "forum$newforumid";

                mkdir ("$dirtomake", 0755);
                
                # Lets add a file to stop snoops, and to use to see if the forum was created
                
                $filetomake = "$dirtomake/index.html";
                open(FILE,">$filetomake");
                print FILE "-";
                close(FILE);
                
                $filetomake = "$dirtomake/.htaccess";
                open(FILE, ">$filetomake");
                  flock (FILE, 2);
                print FILE "AuthUserFile /dev/null\n";
                print FILE "AuthGroupFile /dev/null\n";
                print FILE "AuthName DenyViaWeb\n";
                print FILE "AuthType Basic\n";
                print FILE "\n\n\n\n";
                print FILE "<Limit GET>\n";
                print FILE "order allow,deny\n";
                print FILE "deny from all\n";
                print FILE "</Limit>\n";
                close (FILE);

                $filetoopen = "$ikondir" . "data/allforums.cgi";
                open(FILE, "$filetoopen");
                @forums = <FILE>;
                close(FILE);
   
                
                foreach $line (@forums) {
                    chomp $line;
                    $processed_data .= "$line\n";
                    }
                $processed_data .= "$newforumid|$new_categoryname|$incategory|$new_forumname|$new_forumdescription|$new_forummoderator|$new_htmlstate|$new_idmbcodestate|$new_privateforum|$new_startnewthreads|||0|0|$new_forumgraphic";
                if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
                open(FILE, ">$filetoopen");
                  flock(FILE, 2);
                print FILE $processed_data;
                close(FILE);
                undef $processed_data;
                
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'} / $ibtxt{'2962'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                <font face=verdana color=#333333 size=2>
                ~;

                print "<b>Status</b><p>\n";
                print "<ul>\n";
                if (-e $dirtomake) {
                print "<li><b>$ibtxt{'2963'}</b><p>\n";
                    }
                    else {
                        print "<li><b>$ibtxt{'2964'}</b><p>$ibtxt{'2965'}<p>\n";
                        }
                

                $filetoopen = "$dirtomake/index.html";
                if (-e $filetoopen) {
                    print "<li><b>$ibtxt{'2940'} (index.html) $ibtxt{'2941'}</b><p>\n";
                    }
                    else {
                        print "<li><b>$ibtxt{'2940'} (index.html) $ibtxt{'2942'}</b><p>\n";
                        }
                print "$filetoopen<p>\n";
                print "</ul></td></tr></table></td></tr></table>\n";

} # end routine
        

##################################################################################
######## Subroutes ( Edit Category Name )


sub editcatname {

        
        if ($checkaction ne "yes") {
        
            # Grab the line to edit.
        
            $filetoopen = "$ikondir" . "data/allforums.cgi";
            open(FILE,"$filetoopen") or &systemerror("$ibtxt{'2913'} $filetoopen");
              flock(FILE,2);
            @forums = <FILE>;
            close(FILE);

            foreach $forum (@forums) {
            chomp $forum;
                ($notneeded, $notneeded, $categoryplace) = split(/\|/,$forum);
                    if ($incategory eq "$categoryplace") {
                        ($trash, $categoryname, $notneeded) = split(/\|/,$forum);   
                        }
                    }
        
            # Present the form to be filled in


            print qq~
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="editcatname">
            <input type=hidden name="category" value="$incategory">
            <input type=hidden name="checkaction" value="yes">
            <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
            <b>$ibtxt{'0208'} / $ibtxt{'2904'}</b>
            </td></tr>
            <tr>
        
            <tr>
            <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
            <font face=verdana color=#990000 size=3><b>$ibtxt{'2967'} '$categoryname'</b>
            </td></tr>
                
                
            <tr>
            <td bgcolor=#FFFFFF valign=middle align=left width=40%>
            <font face=verdana color=#333333 size=1><b>$ibtxt{'2959'}</b><br>$ibtxt{'2968'}</font></td>
            <td bgcolor=#FFFFFF valign=middle align=left>
            <input type=text size=40 name="categoryname" value="$categoryname"></td>
            </tr>
            
            
            <tr>
            <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
            <input type=submit value=$ibtxt{'0039'} ></form></td></tr></table></td></tr></table>
            ~;
            } # end if
            
            else {
            
                # Grab the lines to change.
        
                $filetoopen = "$ikondir" . "data/allforums.cgi";
                open(FILE,"$filetoopen") or &systemerror("$ibtxt{'2913'} $filetoopen");
                  flock(FILE,2);
                @forums = <FILE>;
                close(FILE);

               # Lets remake the file with the new info
                
                                $filetoopen = "$ikondir" . "data/allforums.cgi";
                foreach $forum (@forums) {
                chomp $forum;
                ($notneeded, $notneeded, $categorynumber) = split(/\|/,$forum);
                    if ($incategory eq "$categorynumber") {
                        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
                        $linetochange = "$forumid|$new_categoryname|$incategory|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastposter|$lastposttime|$threads|$posts|$forumgraphic"; 
                        chomp $linetochange;
                        $processed_data .= "$linetochange\n";
                        $forumname = ""; $forumdescription = ""; $forummoderator = ""; $lastposter = ""; $lastposttime = ""; $threads = ""; $posts = ""; $forumgraphic = "";
                        }
                        else {
                            $processed_data .= "$forum\n";
                            }
                    }
                if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
                open(FILE,">$filetoopen") or &systemerror("$ibtxt{'2913'} $filetoopen");
                  flock(FILE,2);
                print FILE $processed_data;
                close (FILE);
                undef $processed_data;
                
                
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'} / $ibtxt{'2969'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>$ibtxt{'2102'}</b>
                </td></tr></table></td></tr></table>
                ~;
                
                } # end else
                
            } # end routine


##################################################################################
######## Subroutes ( Edit Category Name )


sub reordercats {

        
        if ($checkaction ne "yes") {

            print qq~
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="reordercategories">
            <input type=hidden name="checkaction" value="yes">
            <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
            <b>$ibtxt{'0208'} / $ibtxt{'2970'}</b>
            </td></tr>
            <tr><td bgcolor=#FFFFFF" colspan=3><font face=verdana size=2 color=#333333>
            <b>$ibtxt{'2902'}</b><br><br>
            $ibtxt{'2971'} <b>$ibtxt{'2972'}</b><br><br>
            <b>$ibtxt{'2973'}</b><br><br>
            <center>$ibtxt{'2974'}</center><br><br>
            </td></tr>
            ~;
            
            $filetoopen = "$ikondir" . "data/allforums.cgi";
            open(FILE, "$filetoopen") or &systemerror("$ibtxt{'2913'} $filetoopen");
            @forums = <FILE>;
            close(FILE);

            foreach $forum (@forums) { #start foreach @forums
                chomp $forum;
                ($forumid, $category, $categoryplace, $forumname, $forumdescription) = split(/\|/,$forum);
                $rearrange = ("$categoryplace|$category|$forumname|$forumdescription|$forumid");
                push (@rearrangedforums, $rearrange);

                } # end foreach (@forums)

            @finalsortedforums = sort(@rearrangedforums);

            foreach $sortedforums (@finalsortedforums) { #start foreach @finalsortedforums

                ($categoryplace, $category) = split(/\|/,$sortedforums);
    
                if ($categoryplace ne $lastcategoryplace) { #start if $categoryplace
                    print qq~
                    <tr>
                    <td bgcolor=#FFFFFF width=40%><font face=verdana color=#333333 size=3>
                    <b>&raquo; $category</b></font></td>
                    <td bgcolor=#FFFFFF><font face=verdana color=#333333 size=2>$ibtxt{'2975'} [ $categoryplace ] - $ibtxt{'2976'} - <input type=text size=4 maxlength=2 name="$categoryplace" value="$categoryplace">
                    </td></tr>
                    ~;
                    } # end if
                    
                    $lastcategoryplace = $categoryplace;
                    
                 } # end foreach
                    
                    
                    
                    print qq~
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <input type=submit value=$ibtxt{'0039'} ></form></td></tr></table></td></tr></table>
                    ~;
                    
            } # end if
    
            
            else {
            
                # Grab the lines to change.
        
                $filetoopen = "$ikondir" . "data/allforums.cgi";
                open(FILE,"$filetoopen") or &systemerror("$ibtxt{'2913'} $filetoopen");
                  flock(FILE,2);
                @forums = <FILE>;
                close(FILE);

                 # Lets remake the file with the new info
                
                foreach $forum (@forums) {
                    chomp $forum;
                    ($notneeded, $notneeded, $categorynumber) = split(/\|/,$forum);
                    $newid = $PARAM{$categorynumber};
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
                    $processed_data .= "$forumid|$category|$newid|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastposter|$lastposttime|$threads|$posts|$forumgraphic\n";
                    }
                if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
                $filetoopen = "$ikondir" . "data/allforums.cgi";
                open(FILE,">$filetoopen") or &systemerror("Cannot Locate $filetoopen");
                 flock(FILE,2);
                print FILE $processed_data;
                close (FILE);
                undef $processed_data;
                
                
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'} / $ibtxt{'2969'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>$ibtxt{'2102'}</b>
                </td></tr></table></td></tr></table>
                ~;
                
                } # end else
            
            
} # end routine

print qq~</td></tr></table></body></html>~;
exit;
