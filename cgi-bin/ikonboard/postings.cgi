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

$thisprog = "postings.cgi";

$query = new CGI;

&checkVALIDITY;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;

for ('forum','topic','membername','password','action','postno', 
     'notify','deletepost','previewfirst','intopictitle','intopicdescription', 
     'inpost','inshowemoticons','inshowsignature','checked','movetoid','leavemessage') {
    next unless defined $_; 
    next if $_ eq 'SEND_MAIL'; 
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
    }


$inforum       = $forum;
$intopic       = $topic;
$inmembername  = $membername;
$inpassword    = $password;
$inpostno      = $postno;
$innotify      = $notify; 
$indeletepost  = $deletepost;
$inleavemessage= $leavemessage;
$currenttime   = time;


# Begin Program

if ($inshowemoticons ne "yes") { $inshowemoticons eq "no"; }
if ($innotify ne "yes")        { $innotify eq "no"; }

if ($checked eq "yes") {
    $namecookie = cookie(-name    =>   "amembernamecookie",
                         -value   =>   "$inmembername",
                         -path    =>   "$cookiepath",
                         -expires =>   "+30d");
    $passcookie = cookie(-name    =>   "apasswordcookie",
                         -value   =>   "$inpassword",
                         -path    =>   "$cookiepath",
                         -expires =>   "+30d");
    print header(-cookie=>[$namecookie, $passcookie]);
    }
    else {
print header('text/html; charset=windows-1251');
        }

if (($inforum)  && ($inforum !~ /^[0-9]+$/))  { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }
if (($intopic ) && ($intopic  !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }
if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }
if (($movetoid) && ($movetoid !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }


    if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
    if (! $inpassword) { $inpassword = cookie("apasswordcookie"); }

    if ($inmembername eq "") {
        $inmembername = "$ibtxt{'0043'}";
        }
        else {
            &getmemberstime("$inmembername");
            }



# Begin Program

    my %Mode = ( 
    'edit'                 =>    \&editform,
    'lock'                 =>    \&lockthread,
    'unlock'               =>    \&unlockthread,        
    'delete'               =>    \&deletethread,
    'movetopic'            =>    \&movetopic,
    'edittopic'		   =>	 \&edit_topic_title
    );


    if($Mode{$action}) { 
        $Mode{$action}->();
        }
        elsif ($action eq "processedit" && $indeletepost eq "yes") { &deletepost;   }
        elsif ($action eq "processedit" && $previewfirst eq "no")  { &processedit;  }
        elsif ($action eq "processedit" && $previewfirst eq "yes") { &editform;     }
        else { &error("$ibtxt{'0901'}&$ibtxt{'1401'}"); }


    &output(
    -Title   => $boardname, 
    -ToPrint => $output, 
    -Version => $versionnumber 
    );


############# subs
sub edit_topic_title {

    &getmember("$inmembername");
    
    &moderator;

    $cleartoedit = "no";
    
    &mischeader("Editing Topic Title");

    #--------------------------
    # Get the old topic details
    # Ensuring we have an old_ prefix for the original data;

            
    my $file = "$ikondir" . "forum$inforum/$intopic.pl";
    open (ENT, $file);
      flock ENT, 1;
    $in = <ENT>;
    close (ENT);

    #          Old title        Old description

    ($topicid, $old_topictitle, $old_topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$in);
        

    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("Editing Topic Title&You are not the forum moderator or board administrator or your password was incorrect"); }
        
        if (($cleartoedit eq "yes") && ($checked eq "yes")) {

        
        #
        # Do we have any data?
        #
    
        unless ($intopictitle) {

            &error("Editing Topic Title&You must enter a topic title!");
        }
	
	$filetoread = "$ikondir" . "forum$inforum/$intopic.thd";
	open DOOR, "$filetoread" or die "Yo, sup: $!";
	  flock (DOOR, 2);
	@file = <DOOR>;
	close DOOR; # it's draughty
	my @edits     = split (/\|/, $file[0]);
	$edits[1] = $intopictitle;
	$file[0] = join "|", @edits;
	
	open (DOOR, ">$filetoread") or die $!;
	  flock (DOOR, 2);
	print DOOR @file;
	close DOOR;

      	open(FILE, ">$file");
          flock(FILE, 2);      # New Title    # New Description
        print FILE "$intopic|$intopictitle|$intopicdescription|$threadstate|$threadposts|$threadviews|$startedby|$startedpostdate|$lastposter|$lastpostdate";
        close(FILE);

        rebuildLIST(-Forum=>"$inforum");
        
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>    
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=2><b>Thread Edited</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>
            Status:
            <ul>
	    <li><a href="$threadprog?forum=$inforum&topic=$intopic">Back to the topic</a>
            <li><a href="$forumsprog?forum=$inforum">Back to the forum</a>
            <li><a href="$forumsummaryprog">Back to the forums</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            ~;
            
            } # end if clear to edit
            
            else {
            
            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="edittopic">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=2><b>Please enter your details to enable moderation mode [ Edit Topic Title ]</b></font></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$ibtxt{'0306'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20> &nbsp; <a href="$registerprog"><font face="$font" color=$fontcolormisc size=1>$ibtxt{'1417'}</font></a></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$ibtxt{'0307'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20> &nbsp; <font face="$font" color=$fontcolormisc size=1><a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$ibtxt{'1415'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="intopictitle" value="$old_topictitle" size=50></font></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$ibtxt{'1416'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="intopicdescription" value="$old_topicdescription" size=50></font></td>
            </tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></form></td></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;
            
             }

} # end edit topic

sub movetopic {
    
    &getmember("$inmembername");
    &moderator;

    $cleartomove = "no";
    
    &mischeader("$ibtxt{'1501'}");
    
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartomove = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartomove = "yes"; }
    unless ($cleartomove eq "yes") { $cleartomove = "no"; }
    
        if ($cleartomove eq "no" && $checked eq "yes") { &error("$ibtxt{'1502'}&$ibtxt{'0504'}"); }    
        
        if (($cleartomove eq "yes") && ($checked eq "yes") && ($movetoid)) {
        
                ### Get a new thread number.

                $dirtoopen = "$ikondir" . "forum$movetoid";
                opendir (DIR, "$dirtoopen"); 
                @numberdata = readdir(DIR);
                closedir (DIR);

                if ($movetoid == $inforum) { &error("$ibtxt{'1502'}&$ibtxt{'1506'} \!"); } 

                @sorteddirdata = grep(/thd/,@numberdata);
                @sorteddirdata = sort numerically(@sorteddirdata);
                @sorteddirdata = reverse(@sorteddirdata);

                $highestno = @sorteddirdata[0];
                $highestno =~ s/.thd//;
                $newthreadnumber = $highestno + 1;
                $currenttime = time;
                
                ### Get the old forum name
                
                $filetoopen = "$ikondir" . "data/allforums.cgi";
                open(FILE, "$filetoopen");
                  flock FILE, 1;
                @forums = <FILE>;
                close(FILE);

                foreach $forumline (@forums) { #start foreach @forums
                    ($tempno, $trash) = split(/\|/,$forumline);
                        if ($inforum eq $tempno) {
                        ($trash, $trash, $trash, $oldforumname, $trash) = split(/\|/,$forumline);
                        }
                    }
                
                ### Get the new forum name
                
                foreach $forumline (@forums) { #start foreach @forums
                    ($tempno, $trash) = split(/\|/,$forumline);
                        if ($movetoid eq $tempno) {
                        ($trash, $trash, $trash, $newforumname, $trash) = split(/\|/,$forumline);
                        }
                    }
                
                unless ($inleavemessage eq "no") {
                
                    $inpost = qq~#Moderation Mode<p>$inpost<p><a href="$boardurl/$threadprog?forum=$movetoid&topic=$newthreadnumber" target="_self">$ibtxt{'1510'}</a>~;
                
                    $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
                    open(FILE, "$filetoopen");
                    @allmessages = <FILE>;
                    close(FILE);
                
                    $linetokeep = @allmessages[0];
                    chomp $linetokeep;
                    ($trash, $topictitle, $trash) = split(/\|/,$linetokeep);
        
                   foreach $messages (@allmessages) {
                            chomp $messages;
                            $processed_data .= "$messages\n";
                            }
                    $processed_data .= "$inmembername|$topictitle|Moderation Mode|yes|yes|$currenttime|$inpost";
                    $filetomake = "$ikondir" . "forum$inforum/$intopic.thd";
                    open(FILE, ">$filetomake");
                      flock(FILE, 2);
                    print FILE $processed_data;
                    close(FILE);
                    undef $processed_data;

                    
                    $threadposts = @allmessages;
                    
                    my $file = "$ikondir" . "forum$inforum/$intopic.pl";
                    open (ENT, $file);
                      flock ENT, 1;
                    $in = <ENT>;
                    close (ENT);

                    ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$in);
        
        
                    open(FILE, ">$file"); 
					flock(FILE, 2); 
					$threadposts++; 
					print FILE "$intopic|$topictitle|$topicdescription|closed|$threadposts|$threadviews|$startedby|$startedpostdate|$lastposter|$lastpostdate"; 
					close(FILE); 


                    
            } # end if inleavemessage eq yes

        my $file = "$ikondir" . "forum$inforum/$intopic.pl";
        open (ENT, $file);
          flock ENT, 1;
        $in = <ENT>;
        close (ENT);

        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$in);
        
        
        my $file = "$ikondir" . "forum$movetoid/$newthreadnumber.pl"; 
		open(FILE, ">$file"); 
		flock(FILE, 2); 
		print FILE "$newthreadnumber|$topictitle|$topicdescription|open|$threadposts|$threadviews|$startedby|$startedpostdate|$lastposter|$lastpostdate"; 
		close(FILE); 


        ### Pick up old forum messages
        
        $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
        open(FILE, "$filetoopen");
        @oldforummessages = <FILE>;
        close(FILE);

        $oldthreadposts = @oldforummessages - 1;
        
         ### Print to new forum message file
        
        foreach $message (@oldforummessages) {
            chomp $message;
            $processed_data .= "$message\n";
            }
        $filetomake = "$ikondir" . "forum$movetoid/$newthreadnumber.thd";
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE $processed_data;
        close(FILE);
        undef $processed_data;


        ### Update the post counts and lastposter details.
        
        $filetoopen = "$ikondir" . "data/allforums.cgi";
        open(FILE, "$filetoopen");
          flock FILE, 1;
        @allforums = <FILE>;
        close(FILE);
        
foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
            ($tempno, $trash) = split(/\|/,$forum);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
                    if ($inleavemessage eq "no") { $threads--; }
                   $currenttime = time; 
					$posts = $posts - $threadposts; 
				#	$posts++;   Иначе перемещение темы считается как пост
					$processed_data .= "$forumid|$category|$categoryplace|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastposter|$lastposttime|$threads|$posts|$forumgraphic\n"; 

                }
                elsif ($movetoid eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
                    $threads++; 
					$posts = $posts + $threadposts; 
					$posts--; 
					$processed_data .= "$forumid|$category|$categoryplace|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastposter|$lastposttime|$threads|$posts|$forumgraphic\n"; 

                    }
            else { $processed_data .= "$forum\n"; }
        }
        if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
        $filetomake = "$ikondir" . "data/allforums.cgi";
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE $processed_data;
        close(FILE);
        undef $processed_data;
        
        
        
        if ($inleavemessage ne "yes") {
        
            ### Delete the old listings first delete the old thread file
            
            $filetounlink = "$ikondir" . "forum$inforum/$intopic.thd";
            unlink $filetounlink;
        
            ### Now we have to trash it from the list.cgi
            
            $filetounlink = "$ikondir" . "forum$inforum/$intopic.pl";
            unlink $filetounlink;

            
            
            } # end unless statement
        
            rebuildLIST(-Forum=>"$inforum");

            rebuildLIST(-Forum=>"$movetoid");
        
        
        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>    
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1503'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
            $ibtxt{'1004'}:
            <ul>
            <li><a href="$forumsprog?forum=$inforum">$ibtxt{'1504'}</a>
            <li><a href="$forumsprog?forum=$movetoid">$ibtxt{'1505'}</a>
            <li><a href="$forumsummaryprog">$ibtxt{'0323'}</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            ~;
            $checked = "no";
        
        } # end clear to move if
        
        else {
        
            $filetoopen = "$ikondir" . "data/allforums.cgi";
            open(FILE, "$filetoopen");
              flock FILE, 1;
            @forums = <FILE>;
            close(FILE);

            $jumphtml .= "<option value=\"\">$ibtxt{'1507'}\n";
            
            foreach $forum (@forums) { #start foreach @forums
                chomp $forum;
                ($movetoforumid, $category, $categoryplace, $forumname, $forumdescription) = split(/\|/,$forum);
                $rearrange = ("$categoryplace|$category|$forumname|$forumdescription|$movetoforumid");
                push (@rearrangedforums, $rearrange);
                } # end foreach (@forums)

            @finalsortedforums = sort numerically(@rearrangedforums);

            foreach $sortedforums (@finalsortedforums) { #start foreach 
            ($categoryplace, $category, $forumname, $forumdescription, $movetoforumid) = split(/\|/,$sortedforums);
    
            if ($categoryplace ne $lastcategoryplace) { #start if $categoryplace
                $jumphtml .= "<option value=\"\">\n";
                $jumphtml .= "<option value=\"\">-- &nbsp; $category\n";
                $jumphtml .= "<option value=\"$movetoforumid\"> $forumname\n";
                }
                else {
                    $jumphtml .= "<option value=\"$movetoforumid\"> $forumname\n";
                    }
                $lastcategoryplace = $categoryplace;
                } # end foreach 
     
            
            
            $output .= qq~

            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
                <tr>
                    <td>
                    <table cellpadding=6 cellspacing=1 border=0 width=100%>
                        <form action="$thisprog" method="post">
                        <input type=hidden name="action" value="movetopic">
                        <input type=hidden name="checked" value="yes">
                        <input type=hidden name="forum" value="$inforum">
                        <input type=hidden name="topic" value="$intopic">
                        <tr>
                        <td bgcolor=$miscbacktwo valign=middle align=center colspan=2><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1508'}</b></font></td></tr>
                            <tr>
                            <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc size=$dfontsize1><center><b>$ibtxt{'1509'}</font></td>
                                <tr>
                                <td bgcolor=$miscbackone valign=middle width=40%><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0306'}</b></font></td>
                                <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20</td></tr>
                                    <tr>
                                    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0307'}</b></font></td>
                                    <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20> &nbsp; <font face="$font" color=$fontcolormisc size=$dfontsize1><a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td></tr>
                                    <tr>
                                    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
                                    <b>$ibtxt{'1513'}</td>
                                    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
                                    <input name="leavemessage" type="radio" value="yes" checked> $ibtxt{'1514'}<br><input name="leavemessage" type="radio" value="no"> $ibtxt{'1515'}</font>
                                    </td>
                                    </tr>
                                <tr>
                                <td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0931'}</b><p>
                                $ibtxt{'1517'}<p>
                                $ibtxt{'1518'}
                                </font></td>
                                <td bgcolor=$miscbackone valign=middle><textarea cols=45 rows=6 wrap="soft" name="inpost"></textarea></td>
                                </tr>
                            <tr>
                        <td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1519'}</b></font></td>
                        <td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><select name="movetoid">$jumphtml</select></font></td>
                        </tr>
                    <tr>
                <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0039'}"></td></tr></form></table></td></tr></table>
            </table>
            </td></tr>
            </table>
            ~;
            
             } # end else

} # end movetopic










sub deletethread {
    
    &getmember("$inmembername");
    &moderator;

    $cleartoedit = "no";
    
    
    &mischeader("$ibtxt{'1512'}");

    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    
        if ($cleartoedit eq "no" && $checked eq "yes") { &error("$ibtxt{'1520'}&$ibtxt{'0504'}"); }
        if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        
        ### Now we have to trash it from the thd's
        
        $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
        open(FILE, "$filetoopen");
        @threads = <FILE>;
        close(FILE);

        $postcount = @threads;
        $postcount--;
        

        $filetotrash = "$ikondir" . "forum$inforum/$intopic.thd";
        unlink "$filetotrash";

        $filetotrash = "$ikondir" . "forum$inforum/$intopic.mal";
        unlink "$filetotrash"; 

        
        ### Now we have to trash it from the list.cgi
            
        $filetotrash = "$ikondir" . "forum$inforum/$intopic.pl";
        unlink $filetotrash;
        
        rebuildLIST(-Forum=>"$inforum");
        
        ### Get the new last forum poster, and post date.
        
        $filetoopen = $ikondir . "forum$inforum/list.cgi";
        open(FILE, $filetoopen);
          flock FILE,1;
        @alltopics = <FILE>;
        close(FILE);
        
        $linetokeep = @alltopics[0];
        chomp $linetokeep;
        ($trash, $trash, $trash, $trash, $trash, $trash, $trash, $trash, $lastforumposter, $lastforumpostdate) = split(/\|/,$linetokeep);
        
        
        $filetoopen = "$ikondir" . "data/allforums.cgi";
        open(FILE, "$filetoopen");
          flock FILE, 1;
        @allforums = <FILE>;
        close(FILE);
        
foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
            ($tempno, $trash) = split(/\|/,$forum);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
                    $posts = $posts - $postcount;
                    $threads--;
                    $processed_data .= "$forumid|$category|$categoryplace|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastforumposter|$lastforumpostdate|$threads|$posts|$forumgraphic\n";
                }
            else { $processed_data .= "$forum\n"; }
        }
        if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
        $filetomake = "$ikondir" . "data/allforums.cgi";
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE $processed_data;
        close(FILE);
        undef $processed_data;

        
        
        require "$ikondir" . "data/boardstats.cgi";
        
        $filetomake = "$ikondir" . "data/boardstats.cgi";
        
        $totalthreads--;
        $totalposts = $totalposts - $postcount;
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
        print FILE "\$totalmembers = \"$totalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);
            
            
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>    
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'1521'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>
            $ibtxt{'1004'}:
            <ul>
            <li><a href="$forumsprog?forum=$inforum">$ibtxt{'0509'}</a>
            <li><a href="$forumsummaryprog">$ibtxt{'1012'}</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$forumsprog?forum=$inforum"> 
            ~;

            } # end if clear to edit
            

            else {
            
            &mischeader("$ibtxt{'1516'}");
            
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="delete">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1522'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1523'}</font></td>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0306'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0307'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20> &nbsp; <font face="$font" color=$fontcolormisc size=1><a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></td></tr></form></table></td></tr></table>
            </table></td></tr></table>
            ~;
            
             }

} # end deletethread



###########################



sub lockthread {

    &getmember("$inmembername");
    
    &moderator;

    $cleartoedit = "no";
    
    
    &mischeader("$ibtxt{'1544'}");

    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("$ibtxt{'1524'}&$ibtxt{'0504'}"); }
        
        if (($cleartoedit eq "yes") && ($checked eq "yes")) {
            
        my $file = "$ikondir" . "forum$inforum/$intopic.pl";
        open (ENT, $file);
          flock ENT, 1;
        $in = <ENT>;
        close (ENT);

        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$in);
        
        open(FILE, ">$file");
          flock(FILE, 2);
        print FILE "$intopic|$topictitle|$topicdescription|closed|$threadposts|$threadviews|$startedby|$startedpostdate|$inmembername|$currenttime";
        close(FILE);

        rebuildLIST(-Forum=>"$inforum");
        
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>    
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1525'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
            $ibtxt{'1004'}:
            <ul>
            <li><a href="$forumsprog?forum=$inforum">$ibtxt{'0509'}</a>
            <li><a href="$forumsummaryprog">$ibtxt{'0323'}s</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            ~;
            
            } # end if clear to edit
            
            else {
            
            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="lock">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1526'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0306'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20> &nbsp; <a href="$registerprog"><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'1417'}</font></a></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0307'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20> &nbsp; <font face="$font" color=$fontcolormisc size=$dfontsize1><a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></form></td></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;
            
             }

} # end lockthread



###########################



sub unlockthread {

    &getmember("$inmembername");
    &moderator;

    $cleartoedit = "no";
    
    
    &mischeader("$ibtxt{'1546'}");

    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    
        if ($cleartoedit eq "no" && $checked eq "yes") { &error("$ibtxt{'1527'}&$ibtxt{'0504'}"); } 
        if (($cleartoedit eq "yes") && ($checked eq "yes")) {
            
        my $file = "$ikondir" . "forum$inforum/$intopic.pl";
        open (ENT, $file);
          flock ENT, 1;
        $in = <ENT>;
        close (ENT);

        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$in);
        
        open(FILE, ">$file");
          flock(FILE, 2);
        print FILE "$intopic|$topictitle|$topicdescription|open|$threadposts|$threadviews|$startedby|$startedpostdate|$inmembername|$currenttime";
        close(FILE);

        rebuildLIST(-Forum=>"$inforum");
        
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>    
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1528'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
            $ibtxt{'1004'}:
            <ul>
            <li><a href="$forumsprog?forum=$inforum">$ibtxt{'0509'}</a>
            <li><a href="$forumsummaryprog">$ibtxt{'0323'}</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            ~;
            } # end if clear to edit
            
            else {
            
            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="unlock">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1538'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0306'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20> &nbsp; <a href="$registerprog"><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'1417'}</font></a></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0307'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20> &nbsp; <font face="$font" color=$fontcolormisc size=$dfontsize1><a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></form></td></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;
            
             }

} # end unlockthread



###########################



sub deletepost {

    $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
    open(FILE, "$filetoopen");
    @allthreads = <FILE>;
    close(FILE);
    
    $posttodelete = $inpostno;
    $posttodelete--;
    $postcountcheck = 0;
    $totalposts = @allthreads;
    

    &getmember("$inmembername");
    &moderator;

    $cleartoedit = "no";
    
    if ($membername eq "$ibtxt{'0043'}") { &error("Posting&Внимание, Гостю запрещено править сообщения"); }
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    
        if ($cleartoedit eq "no" && $checked eq "yes") { &error("$ibtxt{'1529'}&$ibtxt{'0504'}"); }   
        if ($cleartoedit eq "yes") {
            
            if ($posttodelete == 0) { &error("$ibtxt{'1530'}&$ibtxt{'1531'}"); }
            
            ### First off, lets delete the post in the thread.
            
            foreach $postline (@allthreads) {
            chomp $postline;
                unless ($postcountcheck eq $posttodelete) { $processed_data .= "$postline\n"; }
                $postcountcheck++;
                }
            $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
            open(FILE, ">$filetoopen");
              flock(FILE, 2);
            print FILE $processed_data;
            close(FILE);
            undef $processed_data;

        
        $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
        open(FILE, "$filetoopen");
        @allthreads = <FILE>;
        close(FILE);
    
        
        $totalposts = @allthreads;
        $posttograb = $totalposts;
        $posttograb--;
            
        ($postermembername2, $topictitle2, $postipaddress2, $showemoticons2, $showsignature2 ,$postdate2, $post2) = split(/\|/, @allthreads[$posttograb]);

        
        ### Now we have to adjust the post counts.
            
        $filetoopen = "$ikondir" . "forum$inforum/list.cgi";
        open(FILE, $filetoopen);
          flock FILE, 1;
        @alltopics = <FILE>;
        close(FILE);
        
        $count = "0";
        foreach $line (@alltopics) { #start foreach @threads
            ($tempno, $trash) = split(/\|/, $line);
            if ($intopic eq $tempno) {
                $linetokeep = $line;
                $keepcounter = $count;
            }
        $count++;
        } # end foreach
            
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$linetokeep);
        
        $threadposts = $totalposts - 1;
        
       foreach $newline (@alltopics) { #start foreach @threads
        chomp($newline);
            ($tempno, $trash) = split(/\|/,$newline);
            if ($intopic eq $tempno) {
            $processed_data .= "$topicid|$topictitle|$topicdescription|$threadstate|$threadposts|$threadviews|$startedby|$startedpostdate|$postermembername2|$postdate2\n";
            }
        else { $processed_data .= "$newline\n"; }
        }
        if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
        $filetomake = "$ikondir" . "forum$inforum/list.cgi";
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE $processed_data;
        close(FILE);
        undef $processed_data;
        
        
        
        ### Get the new last forum poster, and post date.
        
        $filetoopen = "$ikondir" . "forum$inforum/list.cgi";
        open(FILE, "$filetoopen");
          flock FILE, 1;
        @alltopics = <FILE>;
        close(FILE);
        
        $linetokeep = @alltopics[0];
        chomp $linetokeep;
        
        ($trash, $trash, $trash, $trash, $trash, $trash, $trash, $trash, $lastforumposter, $lastforumpostdate) = split(/\|/,$linetokeep);
        chomp $forumlastposter;
        chomp $forumlastpostdate;
        
        ### Adjust the variables in the Forums Summary Page.
        
        $filetoopen = "$ikondir" . "data/allforums.cgi";
        open(FILE, "$filetoopen");
          flock FILE, 1;
        @allforums = <FILE>;
        close(FILE);
        
foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
            ($tempno, $trash) = split(/\|/,$forum);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
                    $posts--;
                    $processed_data .= "$forumid|$category|$categoryplace|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastforumposter|$lastforumpostdate|$threads|$posts|$forumgraphic\n";
                }
            else { $processed_data .= "$forum\n"; }
        }
        if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
        $filetomake = "$ikondir" . "data/allforums.cgi";
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE $processed_data;
        close(FILE);
        undef $processed_data;

        
        require "$ikondir" . "data/boardstats.cgi";
        
        $filetomake = "$ikondir" . "data/boardstats.cgi";
        $totalposts--;
        
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
        print FILE "\$totalmembers = \"$totalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);
            
            &mischeader("$ibtxt{'1512'}");
            
            
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>    
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'1541'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>
            $ibtxt{'1004'}:
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$intopic">$ibtxt{'1532'}</a>
            <li><a href="$forumsprog?forum=$inforum">$ibtxt{'0509'}</a>
            <li><a href="$forumsummaryprog">$ibtxt{'0323'}</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            ~;

            } # end if clear to edit
            
            else { &error("$ibtxt{'1530'}&$ibtxt{'1533'}"); }



} # end subdelete



###########################



sub editform { # start form



### Grab the post to edit

$filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
open(FILE, "$filetoopen");
@threads = <FILE>;
close(FILE);

$posttoget = $inpostno;
$posttoget--;

($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post) = split(/\|/, @threads[$posttoget]);
        
$post =~ s/\<p\>/\n\n/g;
$post =~ s/\<br\>/\n/g;


### Print form

&getforum("$inforum");
&getmember("$inmembername");

##запрещаем редактировать в закрытой теме посты start
my $ftoopen = "$ikondir" . "forum$inforum/$intopic.pl";
open(FIL, "$ftoopen");
flock (FIL,2);
$in = <FIL>;
close(FIL);
($trash,$trash,$trash,$threadstate,$trash) = split(/\|/,$in);
&error("Редактирование сообщения&Вы не можете редактировать сообщение в закрытой теме")  if (($membercode ne "ad")&&($inmembmod ne "yes")&&($threadstate eq "closed"));
#end
#Запрещаем редактировать посты забаненным start
&error("Редактирование сообщения&Вы забанены")  if ($membercode eq "banned");
##end


if ($allowedentry{$inforum} eq "yes") { $allowed = "yes"; }

if (($privateforum eq "yes") && ($allowed ne "yes")) {
  &error("$ibtxt{'1406'}&$ibtxt{'1407'}");
}   

$rawpost = $post;

if ($previewfirst eq "yes") {
    $rawpost = $inpost;
    $rawpost =~ s/\<p\>/\n\n/g;
    $rawpost =~ s/\<br\>/\n/g;
    &preview;
    }
    else {
        &mischeader("$ibtxt{'1534'}");
        }

if ($emoticons eq "on") {
    $emoticonslink = qq~<a href="javascript:openScript('$miscprog?action=showsmilies',300,350)">$ibtxt{'1408'}</a>~;
    $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>$ibtxt{'1409'}<br>~;
    }


&codebuttons;
$output .= qq~
$headcb
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=4 cellspacing=1 border=0 width=100%>
<tr>
<td bgcolor=$titlecolor colspan=2><font face="$font" color=$titlefontcolor size=1>Topic: $topictitle</td>
</tr>
<tr><form action="$thisprog" method=post name=PostTopic>
<input type=hidden name="action" value="processedit">
<input type=hidden name="postno" value="$inpostno">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
</tr><tr>
<td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0727'}</b></font></td>
<td bgcolor=$miscbackone valign=middle><input type=text size=20 name="membername" value="$inmembername"><font face="$font" color=$fontcolormisc size=$dfontsize1><a ref="$registerprog">$ibtxt{'1417'}</a></font></td>
</tr><tr>
<td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0728'}</b></font></td>
<td bgcolor=$miscbackone valign=middle><input type=password size=20 name="password" value="$inpassword"><font face="$font" color=$fontcolormisc size=$dfontsize1><a ref="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td>
</tr><tr>
<td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1421'}</b><p>
$ibtxt{'1422'} <b>$htmlstate</b> $ibtxt{'1423'}<p>$ibtxt{'1424'} <b>$idmbcodestate</b> $ibtxt{'1423'}<p>$emoticonslink</font></td>
<td bgcolor=$miscbackone valign=middle>$bodycb<TEXTAREA cols=45 name=inpost rows=10 wrap=VIRTUAL>$rawpost</TEXTAREA>$endcb</td>
</tr><tr>
<td bgcolor=$miscbacktwo valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1425'}</b>
</font></td>
<td bgcolor=$miscbacktwo valign=middle><input type=checkbox name="inshowsignature" value="yes" checked>
<font face="$font" color=$fontcolormisc size=1>$ibtxt{'1426'}<br>
$emoticonsbutton
<b>$ibtxt{'1427'}</b><input name="previewfirst" type="radio" value="yes"> $ibtxt{'0130'} &nbsp; <input name="previewfirst" type="radio" value="no" checked> $ibtxt{'0129'}
</font></td>
</tr>
<tr>
<td bgcolor=$miscbackone valign=middle align=left valign=middle>
<font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1536'}</b></td>
<td bgcolor=$miscbackone valign=middle align=left valign=middle>
<font face="$font" color=$fontcolormisc size=$dfontsize1>
<input type=checkbox name="deletepost" value="yes">$ibtxt{'1535'}
</font></td></tr>
<tr>
<td bgcolor=$miscbackone valign=middle colspan=2 align=center>
<input type=Submit value=$ibtxt{'0039'} name=Submit> &nbsp; <input type="reset" name="Clear">
</form>
</td></tr></table></tr></td></table>
~;

} # end edit form



###########################



sub processedit {

            $posttoget = $inpostno;
            $posttoget--;
            $postcountcheck = 0;

            $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
            open(FILE, "$filetoopen");
            @allthreads = <FILE>;
            close(FILE);
            
            ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post) = split(/\|/, @allthreads[$posttoget]);



            &getmember("$inmembername");
            &moderator;

            &getforum("$inforum");
            
            if ($allowedentry{$inforum} eq "yes") { $allowed = "yes"; }

            if (($privateforum eq "yes") && ($allowed ne "yes")) {
                &error("$ibtxt{'1406'}&$ibtxt{'1407'}");
                }   

            $cleartoedit = "no";

            if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
            if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
            if (($inmembername eq $postermembername) && ($inpassword eq $password)) { $cleartoedit = "yes"; }

            if ($inmembername eq "$ibtxt{'0043'}"){$cleartoedit = "no"} 

        unless ($cleartoedit eq "yes") { $cleartoedit eq "no"; }
        
        if ($cleartoedit eq "yes") {
            
            $editpostdate = time;
            $editpostdate = $editpostdate + ($timezone*3600) + ($timedifferencevalue*3600);
            $editpostdate = &dateformat("$editpostdate");

            $inpost =~ s/\t//g;
            $inpost =~ s/\r//g;
            $inpost =~ s/  / /g;
            $inpost =~ s/\n\n/\<p\>/g;
            $inpost =~ s/\n/\<br\>/g;
            

            # Open the bad word filter
        
            $filetoopen = "$ikondir" . "data/badwords.cgi";
            open (FILE, "$filetoopen");
            $badwords = <FILE>;
            close (FILE);
            
            if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                $inpost =~ s/$bad/$good/ig;
                }
             }
            unless ($membercode eq "ad") {
                $inpost = qq~$inpost<p>[s]($ibtxt{'1537'} $inmembername $ibtxt{'0010'} $editpostdate)[/s]~;
                }
                
foreach $postline (@allthreads) {
            chomp $postline;
                if ($postcountcheck eq $posttoget) {
                    $processed_data .= "$postermembername|$topictitle|$postipaddress|$inshowemoticons|$inshowsignature|$postdate|$inpost\n";
                    }
                else { $processed_data .= "$postline\n"; }
                $postcountcheck++;
                }
            $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
            open(FILE, ">$filetoopen");
              flock(FILE, 2);
            print FILE $processed_data;
            close(FILE);
            undef $processed_data;

            &mischeader("$ibtxt{'1542'}");
            my $gotopage = ($pagestart - $maxthreads);
            $gotopage = 0 unless $gotopage > 0;
            $relocurl = "$threadprog?forum=$inforum&topic=$intopic&start=$gotopage";
            
            
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>    
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1543'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
            $ibtxt{'1004'}:
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$intopic">$ibtxt{'1532'}</a>
            <li><a href="$forumsprog?forum=$inforum">$ibtxt{'0509'}</a>
            <li><a href="$forumsummaryprog">$ibtxt{'0323'}</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;
            
            } # end if clear to edit
            
            else { &error("$ibtxt{'1539'}&$ibtxt{'1540'}"); }

} # end routine



