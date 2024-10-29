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

$|++;                                    # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "messenger.cgi";

$query = new CGI;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;

$intouser         = $query -> param('touser');
$action           = $query -> param('action');
$inmsg            = $query -> param('msg');
$inwhere          = $query -> param('where');
$inmembername     = $query -> param('membername');
$inpassword       = $query -> param('password');
$inmsgtitle       = $query -> param('msgtitle');
$inmessage        = $query -> param('message');


$inmembername        = &cleaninput($inmembername);
$inpassword          = &cleaninput($inpassword);
$inmessage           = &cleaninput($inmessage);
$inmsgtitle          = &cleaninput($inmsgtitle);

$inboxpm = qq~<img src="$imagesurl/images/inboxpm.jpg" border=0>~;
$outboxpm = qq~<img src="$imagesurl/images/outboxpm.jpg" border=0>~;
$newpm = qq~<img src="$imagesurl/images/newpm.jpg" border=0>~;
$replypm = qq~<img src="$imagesurl/images/replypm.jpg" border=0>~;
$deletepm = qq~<img src="$imagesurl/images/deletepm.jpg" border=0>~;

###Begin Program

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie");   }


if ($inmembername eq "" || $inmembername eq "Guest") {
$inmembername = "Guest";
&messengererror("Личный ящик&Гости не могут пользоваться личным ящиком");    
    }

&getmember("$inmembername");  
&messengererror("Личный ящик&Вы забанены") if ($membercode eq "banned");     

if ($action eq "loggedin") {
$namecookie = cookie(-name    =>   "amembernamecookie",
                     -value   =>   "$inmembername",
                     -path    =>   "$cookiepath",
                     -expires =>   "+30d");
$passcookie = cookie(-name    =>   "apasswordcookie",
                     -value   =>   "$inpassword",
                     -path    =>   "$cookiepath",
                     -expires =>   "+30d");

print header(-cookie  =>[$namecookie, $passcookie]);
}
else {
print header('text/html; charset=windows-1251');
    }

if (($inmsg) && ($inmsg !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}"); }

&messengererror("Отправка сообщения&Вы не можете отправить сообщение Гостю") if ($intouser eq "Guest");
### Print Header for the page.

    $output .= qq~
    <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
        <tr>
            <td>
                <table cellpadding=3 cellspacing=1 border=0 width=100%>
                ~;
    
### Startactions



    if ($action eq "new") {
    
    
            # Validate user
    
            &getmember("$inmembername");
    
            if ($userregistered eq "no") {  &messengererror("$ibtxt{'0107'}&$ibtxt{'1102'}"); }
            elsif ($inpassword ne $password) {  &messengererror("$ibtxt{'0107'}&$ibtxt{'0303'}"); }
            elsif ($inmembername eq "") { &login("$thisprog?action=reply&touser=$intouser"); }
        
            
            $cleanname = $intouser;
            $cleanname =~ s/\_/ /g;

            # Present the form

            $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=3><font face="$font" color=$fontcolormisc size=3><b>$ibtxt{'1104'}</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle align=center colspan=3><a href="$thisprog?action=inbox">$inboxpm</a> &nbsp; <a href="$thisprog?action=outbox">$outboxpm</a> &nbsp; <a href="$thisprog?action=new">$newpm</a></td>
            </tr>
            <tr>
            
            <form action="$thisprog" method=post>
            <input type=hidden name="action" value="send">
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'1105'}</b></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$ibtxt{'1106'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="touser" value="$cleanname" size=40></a></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'1107'}</b></font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="msgtitle" size=40 maxlength=80></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'1108'}</b></td>
            <td bgcolor=$miscbackone valign=middle><textarea cols=40 rows=6 name="message"></textarea></td>
            </tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
            <input type=Submit value=$ibtxt{'0039'} name="Submit"> &nbsp; <input type="reset" name="Clear"></form>
            </td></tr>
            ~;  
    
            
    } # end action
    
    
    elsif ($action eq "reply1") {
    
    
            # Validate user
    
            &getmember("$inmembername");
    
            if ($userregistered eq "no") {  &messengererror("$ibtxt{'0107'}&$ibtxt{'1102'}"); }
            elsif ($inpassword ne $password) {  &messengererror("$ibtxt{'0107'}&$ibtxt{'0303'}"); }
            elsif ($inmembername eq "") { &login("$thisprog?action=reply&touser=$intouser"); }
            
            
             # Pick up the messages (inbox)
        
        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
        
        $filetoopen = "$ikondir". "messages/$memberfilename" . "_msg.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen");
        @inboxmessages = <FILE>;
        close (FILE);
        
        # Get the line to split
        
        $msgtograb = @inboxmessages[$inmsg];
        
        ($from, $readstate, $date, $messagetitle, $post) = split(/\|/,$msgtograb);      
        
            
            $cleanname = $intouser;
            $cleanname =~ s/\_/ /g;
            $post =~ s/\<br\>/\n/g;
            $post =~ s/\<p\>/\n\n/g;

            # Present the form

            $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=3><font face="$font" color=$fontcolormisc size=3><b>$ibtxt{'1104'}</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle align=center colspan=3><a href="$thisprog?action=inbox">$inboxpm</a> &nbsp; <a href="$thisprog?action=outbox">$outboxpm</a> &nbsp; <a href="$thisprog?action=new">$newpm</a></td>
            </tr>
            <tr>
            
            <form action="$thisprog" method=post>
            <input type=hidden name="action" value="send">
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'1105'}</b></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$ibtxt{'1106'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="touser" value="$from" size=40></a></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'1107'}</b></font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="msgtitle" value="RE:$messagetitle" size=40 maxlength=80></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'1108'}</b></td>
            <td bgcolor=$miscbackone valign=middle><textarea cols=40 rows=6 name="message">\[quote\]$post\[/quote\]\n</textarea></td>
            </tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
            <input type=Submit value=$ibtxt{'0039'} name="Submit"> &nbsp; <input type="reset" name="Clear"></form>
            </td></tr>
            ~;  
    
            
    } # end action



    elsif ($action eq "outbox") {
    
        
        # Validate the user
    
        &getmember("$inmembername");
    
        if ($userregistered eq "no") { &messengererror("$ibtxt{'1127'}&$ibtxt{'1102'}"); }
        elsif ($inpassword ne $password) { &messengererror("$ibtxt{'1127'}&$ibtxt{'0303'}"); }
        elsif ($inmembername eq "") { &login("$thisprog?action=outbox"); }
        
        
        # Pick up the messages (outbox)
        
        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
        
        $filetoopen = "$ikondir". "messages/$memberfilename" . "_out.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen");
        @outboxmessages = <FILE>;
        close (FILE);
        
        $totalinboxmessages = @outboxmessages;
        
        $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=2><font face="$font" color=$fontcolormisc size=3><b>$ibtxt{'1110'} $membername</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle align=center colspan=3><a href="$thisprog?action=inbox">$inboxpm</a> &nbsp; <a href="$thisprog?action=outbox">$outboxpm</a> &nbsp; <a href="$thisprog?action=new">$newpm</a></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone align=center valign=middle><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'1112'}</b></td>
                <td bgcolor=$miscbackone align=center valign=middle><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'2404'}</b></td>
            </tr>
            ~;
        
        
        # Display the messages.
        
        $count = 0;
        
        foreach (@outboxmessages) {
            ($from, $readstate, $date, $messagetitle, $message) = split(/\|/,$_);
            if ($readstate eq "no") {
                $readstate = qq~<font face="$font" color="$fonthighlight" size=1><b>no</b></font>~;
                }
                else {
                    $readstate = qq~<font face="$font" color="$fontcolormisc" size=1>yes</font>~;
                    }
            
                $output .= qq~
                <tr>
                    <td bgcolor=$miscbackone align=center valign=middle><font face="$font" color=$fontcolormisc size=1>$from</td>
                    <td bgcolor=$miscbackone align=center valign=middle><font face="$font" color=$fontcolormisc size=1><a href="$thisprog?action=outread&msg=$count">$messagetitle</a></td>
                </tr>
                ~;
            $count++;
            } # end foreach
            
            $output .=qq~
                <tr>
                <td bgcolor=$miscbacktwo align=center valign=middle colspan=2><font face="$font" color=$fontcolormisc size=2><a href="$thisprog?action=deleteall&where=outbox">$ibtxt{'1140'}</a></td>
                </tr>
                ~;
            
    } # end action
    
    
    
    elsif ($action eq "deleteall") {
        
            # Validate user
    
            &getmember("$inmembername");
    
            if ($userregistered eq "no") { &messengererror("$ibtxt{'0107'}&$ibtxt{'1102'}"); }
            elsif ($inpassword ne $password) { &messengererror("$ibtxt{'0107'}&$ibtxt{'0303'}"); }
            elsif ($inmembername eq "") { &login("$thisprog?action=deleteall&where=$inwhere"); }
            
            
            # Ensure the username has the underscore returned
            
            $memberfilename = $inmembername;
            $memberfilename =~ s/ /\_/g;
            
            
            # Open the user's file
            
            if ($inwhere eq "inbox") {
                $filetotrash = "$ikondir". "messages/$memberfilename" . "_msg.cgi";
                }
                elsif ($inwhere eq "outbox") {
                    $filetotrash = "$ikondir". "messages/$memberfilename" . "_out.cgi";
                    }
            
            if ($filetotrash ne "") {
                unlink "$filetotrash";
                }
                else {
                    &messengererror("$ibtxt{'0107'}&$ibtxt{'1114'}, $ibtxt{'1115'}");
                    }
                
            
            
            
            # Print the all done screen
            
            $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc size=3><b>$ibtxt{'1116'}</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle align=center><a href="$thisprog?action=inbox">$inboxpm</a> &nbsp; <a href="$thisprog?action=outbox">$outboxpm</a> &nbsp; <a href="$thisprog?action=new">$newpm</a></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'1117'} $inwhere</b></td>
            </tr>
            ~;
            
        } # end action
    
    
    



    elsif ($action eq "outread") { # start showing messages
    
    
        # Validate the user
    
        &getmember("$inmembername");
    
        if ($userregistered eq "no") { &messengererror("$ibtxt{'0107'}&$ibtxt{'1102'}"); }
        elsif ($inpassword ne $password) { &messengererror("$ibtxt{'0107'}&$ibtxt{'0303'}"); }
        elsif ($inmembername eq "") { &login("$thisprog?action=outread&msg=$inmsg"); }
        
        # Pick up the messages (outbox)
        
        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
        
        
        $filetoopen = "$ikondir". "messages/$memberfilename" . "_out.cgi";
        open (FILE, "$filetoopen");
        @outboxmessages = <FILE>;
        close (FILE);
        
        # Get the line to split
        
        $msgtograb = @outboxmessages[$inmsg];
        
        ($to, $readstate, $date, $messagetitle, $post) = split(/\|/,$msgtograb);        
    
        $date = $date + ($timedifferencevalue*3600) + ($timezone*3600);
        $date = &dateformat("$date");
        $cleanmember = $to;
        $cleanmember =~ s/ /\_/g;
        
        
        # Print the header
        $post_reply = $post;

        $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=3><font face="$font" color=$fontcolormisc size=3><b>$ibtxt{'1110'} $membername</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle align=center colspan=3><a href="$thisprog?action=delete&where=outbox&msg=$inmsg">$deletepm</a> &nbsp; <a href="$thisprog?action=inbox">$inboxpm</a> &nbsp; <a href="$thisprog?action=outbox">$outboxpm</a> &nbsp;<a href="$thisprog?action=new">$newpm</a> &nbsp;<a href="$thisprog?action=reply1&msg=$inmsg">$replypm</a</td>
            </tr>
            ~;
        
        
        # Split the line
        
                $post = &ikoncode("$post");
                
                if ($emoticons eq "on") {
                    &doemoticons("$post");
                
                    $post =~ s/\:\)/<img src=\"$imagesurl\/emoticons\/smile.gif\" border=\"0\">/g;
                    $post =~ s/\;\)/<img src=\"$imagesurl\/emoticons\/wink.gif\" border=\"0\">/g;
                    $post =~ s/\:\(/<img src=\"$imagesurl\/emoticons\/sad.gif\" border=\"0\">/g;
                    $post =~ s/\:\o/<img src=\"$imagesurl\/emoticons\/shocked.gif\" border=\"0\">/g;
                    }
                    
    
            ### Print message
    
            $output .= qq~
                <tr>
                    <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=1>
                    $ibtxt{'1118'} <b>$to</b> $ibtxt{'1119'} <b>$date</b></font></td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone valign=top align=left><font face="$font" color=$fontcolormisc size=1>
                    <b>$ibtxt{'1107'}: $messagetitle</b><p>
                    $post</td>
                </tr>
                ~;

            
    } # end outread








    elsif ($action eq "send") {
    
            # Check to make sure the user exists
            
            &gettopicmember("$intouser");
            
            if ($userregistered eq "no") { &messengererror("$ibtxt{'1120'}&$ibtxt{'1121'}"); }
    
            # Validate user
    
            &getmember("$inmembername");
    
            if ($userregistered eq "no") { &messengererror("$ibtxt{'0107'}&$ibtxt{'1102'}"); }
            elsif ($inpassword ne $password) { &messengererror("$ibtxt{'0107'}&$ibtxt{'0303'}"); }
            elsif ($inmembername eq "") { &login("$thisprog?action=reply&touser=$intouser"); }
            
            # Check for blanks
            
            if ($inmsgtitle eq "") { $blanks = "yes"; }
            if ($inmessage eq "") { $blanks = "yes"; }
            if ($intouser eq "") { $blanks = "yes"; }
            
            if ($blanks eq "yes") { &messengererror("$ibtxt{'1120'}&$ibtxt{'1122'}"); }
       
        
            # Ensure the username has the underscore returned
            
            $memberfilename = $intouser;
            $memberfilename =~ s/ /\_/g;
            $currenttime = time;
            
            
            # Send the message to the user's file
            
            $filetoopen = "$ikondir". "messages/$memberfilename" . "_msg.cgi";
            $filetoopen = &stripMETA($filetoopen);
            open (FILE, "$filetoopen");
            @inboxmessages = <FILE>;
            close (FILE);
        
            # Write back to the 'to' users file
        
            open (FILE, ">$filetoopen");
              flock (FILE, 2);
            print FILE "$membername|no|$currenttime|$inmsgtitle|$inmessage\n";
            foreach $line (@inboxmessages) {
                chomp $line;
                print FILE "$line\n";
                }
            close (FILE);
            
            # Now, write it to the outbox of the sender
            
            $memberfilename = $inmembername;
            $memberfilename =~ s/ /\_/g;
            
            $filetoopen = "$ikondir". "messages/$memberfilename" . "_out.cgi";
            $filetoopen = &stripMETA($filetoopen);
            open (FILE, "$filetoopen");
            @outboxmessages = <FILE>;
            close (FILE);
        
            open (FILE, ">$filetoopen");
              flock (FILE, 2);
            print FILE "$intouser|yes|$currenttime|$inmsgtitle|$inmessage\n";
            foreach $line (@outboxmessages) {
                chomp $line;
                print FILE "$line\n";
                }
            close (FILE);
            
            # create the dummy file
            
            
            
            # Print the all done screen
            
            $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc size=3><b>$ibtxt{'1123'}</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle align=center><a href="$thisprog?action=inbox">$inboxpm</a> &nbsp; <a href="$thisprog?action=outbox">$outboxpm</a> &nbsp; <a href="$thisprog?action=new">$newpm</a></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'1124'} $intouser $ibtxt{'1125'}</b><p>$ibtxt{'1126'}</td>
            </tr>
            ~;
            
            
    } # end action
            
            

    
    
    
    

    
    elsif ($action eq "loggedin") {
    
        # Validate user
    
        &getmember("$inmembername");
    
        if ($userregistered eq "no") { &messengererror("$ibtxt{'1127'}&$ibtxt{'1102'}"); }
        elsif ($inpassword ne $password) { &messengererror("$ibtxt{'1127'}&$ibtxt{'0303'}"); }
        elsif ($inmembername eq "") { &login("$thisprog?action=loggedin"); }
        
        
        # Pick up the messages
        
        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
        
        $filetoopen = "$ikondir". "messages/$memberfilename" . "_msg.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen");
        @allmessages = <FILE>;
        close (FILE);
        
        $totalmessages = @allmessages;
        
        $unread = 0;
        
        foreach (@allmessages) {
            ($from, $readstate, $date, $messagetitle, $message) = split(/\|/,$_);
            if ($readstate eq "no") {
                $unread++;
                }
            }
            
        if ($unread eq "0") { $unread eq "no"; }
        
        
        $output .= qq~
        <tr>
            <td bgcolor=$miscbacktwo  align=center><font face="$font" color=$fontcolormisc size=3><b>$ibtxt{'1128'} $membername</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle align=center><a href="$thisprog?action=inbox">$inboxpm</a> &nbsp; <a href="$thisprog?action=outbox">$outboxpm</a> &nbsp; <a href="$thisprog?action=new">$newpm</a></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle align=center>
                <font face="$font" color=$fontcolormisc size=2><p>
                $ibtxt{'1129'} <b>$totalmessages</b> $ibtxt{'1130'}<p>
                $ibtxt{'1131'} <b><font color="$fonthighlight">$unread</b><font color=$fontcolormisc> $ibtxt{'1132'}
                <p>
                <font size=1>
                <blockquote><b>$ibtxt{'1133'}</b> $ibtxt{'1134'}</blockquote></font>
                </td></tr>
            <tr>
            ~;
        
    
    } # end action
    
    
    


    elsif ($action eq "inbox") {
    
        # Validate the user
    
        &getmember("$inmembername");
    
        if ($userregistered eq "no") { &messengererror("$ibtxt{'1127'}&$ibtxt{'1102'}"); }
        elsif ($inpassword ne $password) { &messengererror("$ibtxt{'1127'}&$ibtxt{'0303'}"); }
        elsif ($inmembername eq "") { &login("$thisprog?action=loggedin"); }
        
        
        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
        
        # Pick up the messages (inbox)
        
        $filetoopen = "$ikondir". "messages/$memberfilename" . "_msg.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen");
        @inboxmessages = <FILE>;
        close (FILE);
        
        $totalinboxmessages = @inboxmessages;
        
        $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=3><font face="$font" color=$fontcolormisc size=3><b>$ibtxt{'1111'} $membername</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle align=center colspan=3><a href="$thisprog?action=inbox">$inboxpm</a> &nbsp; <a href="$thisprog?action=outbox">$outboxpm</a> &nbsp; <a href="$thisprog?action=new">$newpm</a></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone align=center valign=middle><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'0934'}</b></td>
                <td bgcolor=$miscbackone align=center valign=middle><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'2404'}</b></td>
                <td bgcolor=$miscbackone align=center valign=middle><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'1137'}</b></td>
            </tr>
            ~;
        
        
        # Display the messages.
        
        $count = 0;
        
        foreach (@inboxmessages) {
            ($from, $readstate, $date, $messagetitle, $message) = split(/\|/,$_);
            if ($readstate eq "no") {
                $readstate = qq~<font face="$font" color="$fonthighlight" size=1><b>$ibtxt{'0129'}</b></font>~;
                }
                else {
                    $readstate = qq~<font face="$font" color="$fontcolormisc" size=1>$ibtxt{'0130'}</font>~;
                    }
            
                $output .= qq~
                <tr>
                    <td bgcolor=$miscbackone align=center valign=middle><font face="$font" color=$fontcolormisc size=1>$from</td>
                    <td bgcolor=$miscbackone align=center valign=middle><font face="$font" color=$fontcolormisc size=1><a href="$thisprog?action=read&msg=$count">$messagetitle</a></td>
                    <td bgcolor=$miscbackone align=center valign=middle>$readstate</td>
                </tr>
                ~;
            $count++;
            } # end foreach
            
            $output .= qq~
                <tr>
                <td bgcolor=$miscbacktwo align=center valign=middle colspan=3><font face="$font" color=$fontcolormisc size=2><a href="$thisprog?action=deleteall&where=inbox">$ibtxt{'1140'}</a></td>
                </tr>
                ~;
            
    } # end action




    
    elsif ($action eq "read") { # start showing messages
    
    
    # Validate the user
    
        &getmember("$inmembername");
    
        if ($userregistered eq "no") { &messengererror("$ibtxt{'0107'}&$ibtxt{'1102'}"); }
        elsif ($inpassword ne $password) { &messengererror("$ibtxt{'0107'}&$ibtxt{'0303'}"); }
        elsif ($inmembername eq "") { &login("$thisprog?action=read&msg=$inmsg"); }
        
        
        # Pick up the messages (inbox)
        
        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
        
        $filetoopen = "$ikondir". "messages/$memberfilename" . "_msg.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen");
        @inboxmessages = <FILE>;
        close (FILE);
        
        # Get the line to split
        
        $msgtograb = @inboxmessages[$inmsg];
        
        ($from, $readstate, $date, $messagetitle, $post) = split(/\|/,$msgtograb);      
    
        
        
        # Write back to as read
        
        $count = 0;
        
        open (FILE, ">$filetoopen");
          flock (FILE, 2);
        foreach $line (@inboxmessages) {
            chomp $line;
            if ($count eq $inmsg) {
                print FILE "$from|$ibtxt{'0130'}|$date|$messagetitle|$post";
                }
                else {
                    print FILE "$line\n";
                    }
                $count++;
                }
        close (FILE);
        
        $date = $date + ($timedifferencevalue*3600) + ($timezone*3600);
        $date = &dateformat("$date");
        $cleanmember = $from;
        $cleanmember =~ s/ /\_/g;
        
        
        # Print the header
        
        $post_reply = $post;
        $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=3><font face="$font" color=$fontcolormisc size=3><b>$ibtxt{'1111'} $membername</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle align=center colspan=3><a href="$thisprog?action=delete&where=inbox&msg=$inmsg">$deletepm</a> &nbsp; <a href="$thisprog?action=inbox">$inboxpm</a> &nbsp; <a href="$thisprog?action=outbox">$outboxpm</a> &nbsp;<a href="$thisprog?action=new">$newpm</a> &nbsp;<a href="$thisprog?action=reply1&msg=$inmsg">$replypm</a</td>
            </tr>
            ~;
        
        
        # Split the line
                
                $post = &ikoncode("$post");
                
                if ($emoticons eq "on") {
                    $post = &doemoticons("$post");
                
                    $post =~ s/\:\)/<img src=\"$imagesurl\/emoticons\/smile.gif\" border=\"0\">/g;
                    $post =~ s/\;\)/<img src=\"$imagesurl\/emoticons\/wink.gif\" border=\"0\">/g;
                    $post =~ s/\:\(/<img src=\"$imagesurl\/emoticons\/sad.gif\" border=\"0\">/g;
                    $post =~ s/\:\o/<img src=\"$imagesurl\/emoticons\/shocked.gif\" border=\"0\">/g;
                    }
                    
    
            ### Print message
    
            $output .= qq~
                <tr>
                    <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=1>
                    $ibtxt{'1141'} <b>$from</b> $ibtxt{'1142'} <b>$date</b></font></td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone valign=top align=left><font face="$font" color=$fontcolormisc size=1>
                    <b>$ibtxt{'1107'}: $messagetitle</b><p>
                    $post</td>
                </tr>
                ~;

            
    } # end read
    
    
    
    
    
    elsif ($action eq "delete") {
    
    
            # Validate user
    
            &getmember("$inmembername");
    
            if ($userregistered eq "no") { &messengererror("$ibtxt{'0107'}&$ibtxt{'1102'}"); }
            elsif ($inpassword ne $password) { &messengererror("$ibtxt{'0107'}&$ibtxt{'0303'}"); }
            elsif ($inmembername eq "") { &login("$thisprog?action=delete&where=$inwhere&msg=$inmsg"); }
        
            
            # Ensure the username has the underscore returned
            
            $memberfilename = $inmembername;
            $memberfilename =~ s/ /\_/g;
            
            
            # Open the user's file
            
            if ($inwhere eq "inbox") {
                $filetoopen = "$ikondir". "messages/$memberfilename" . "_msg.cgi";
                }
                elsif ($inwhere eq "outbox") {
                    $filetoopen = "$ikondir". "messages/$memberfilename" . "_out.cgi";
                    }
            
            $filetoopen = &stripMETA($filetoopen);
            open (FILE, "$filetoopen");
            @boxmessages = <FILE>;
            close (FILE);
        
            # Write back to the 'to' users file
            
            $count = 0;
        
            open (FILE, ">$filetoopen");
              flock (FILE, 2);
            foreach $line (@boxmessages) {
                chomp $line;
                if ($count ne $inmsg) {
                    print FILE "$line\n";
                    }
                $count++;
                }
            close (FILE);
            
            
            # Print the all done screen
            
            $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc size=3><b>$ibtxt{'1143'}</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle align=center><a href="$thisprog?action=inbox">$inboxpm</a> &nbsp; <a href="$thisprog?action=outbox">$outboxpm</a> &nbsp; <a href="$thisprog?action=new">$newpm</a></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'1144'} $inwhere</b></td>
            </tr>
            ~;
            
            
    } # end action
    
    
    
    
    
    else {
    
        &login("$thisprog?action=loggedin");
        
        }





            $output .= qq~</table></td></tr></table>~;

            &printmessenger(
            -Title   => "$boardname - $ibtxt{'0107'}", 
            -ToPrint => $output, 
            -Version => $versionnumber 
            );



##############################################################
### Sub route (login)

    
sub login {

	local($url) = @_;
	
    ($postto, $therest) = split(/\?/,$url);
    
    @pairs = split(/\&/,$therest);
    
    foreach (@pairs) {
        ($name, $value)=split(/\=/,$_);
        $hiddenvars .= qq~<input type=hidden name="$name" value="$value">\n~;
        }
           
	        
	    $output .= qq~
	    <form action="$postto" method="post">$hiddenvars
	        <tr>
	            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'0801'}</b></font></td></tr>
	        <tr>
	            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$ibtxt{'0306'}</font></td>
	            <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20></td></tr>
	        <tr>
	            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$ibtxt{'0307'}</font></td>
	            <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20></td></tr>
	        <tr>
	            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></td></tr></table></td></tr></table>
	        ~;
	        
	 } # end routine 
 

