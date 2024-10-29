#!/usr/bin/perl

#############################################################
#
# >>>>>> SET UP ASSISTANT
#
#
# Ikonboard v2.1
# Copyright 2000 Ikonboard.com - All Rights Reserved
# Ikondiscussion is a trademark of Ikonboard.com
#
# Software Distributed by: Ikonboard.com
# Visit us online at http://www.ikonboard.com
# Email us on boards@ikonboard.com
#
# All files written by Matthew Mecham
#############################################################
use CGI::Carp "fatalsToBrowser";
use CGI qw(:standard);

$query = new CGI;
@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        $theparam =~ s/\@/\\\@/g;
		      ${$param} = $theparam;
        if ($param ne "action") {
            $printme .= "\$" . "$param = \"$theparam\"\;\n";
            }
	}
$stylesheet =<<__end_of_sheet__;
<!--
textarea, input {   FONT-FAMILY:verdana,arial;color:#000000; FONT-SIZE: 14px; background-color:#FFFFFF; width:500px  }
SELECT, option {   FONT-FAMILY:verdana,arial;color:#000000; FONT-SIZE: 14px; background-color:#eeeeee }

-->
__end_of_sheet__

$thisprog = "install.cgi"; $|=1; 
if ($action ne "final_step" || !$action) { print header('text/html; charset=windows-1251'); print start_html(-title=>"Помощник установки Ikonboard", -bgcolor=>"#EEEEEE", -style=>{-code=>$stylesheet}); }

if ($action eq "step_two") {

$endprint = "1\;\n";

$errorflag = 0;

        $filetomake = "$ikondir" . "data/boardinfo.cgi";

        open(FILE,">$filetomake");
        flock(FILE,2);
        print FILE "$printme";
        print FILE "\$dfontsize1 = \"1\"\;\n";
       	print FILE "\$dfontsize2 = \"2\"\;\n";
       	print FILE "\$dfontsize3 = \"3\"\;\n";
       	print FILE "\$dfontsize4 = \"4\"\;\n";
        print FILE "\$char_in_topic = \"80\"\;\n";
        print FILE "\$char_locat_in_topic = \"18\"\;\n";
        print FILE $endprint;
        close(FILE);
        
        
        if (-e $filetomake && -w $filetomake) {
            $saved_variables = qq(<font face="verdana" size="3" color="#0000FF">Все выбранные сведения полностью записаны в $ikondir data/boardinfo.cgi.</font>);
            }
            else {
                $saved_variables = qq(<font face="verdana" size="3" color="#FF0000">Извините. Я не могу сохранить сведения.
                                      Вы выбрали $ikondir/data путём к папке 'data'. Это верно?
                                      Если это так, проверьте CHMOD на папке 'data' и воспользуйтесь кнопкой НАЗАД
                                      для возврата в форму и перезаписи);
                                       $errorflag = "1";
                }
      
        $filetocheck = "$ikondir" . "ikonboard.cgi";
        if (-e $filetocheck) {
            $found_cgi = qq(<font face="verdana" size="2" color="#0000FF">Правильно - найден $filetocheck</font>);
            }
            else {
                $errorflag = "1"; $found_cgi = qq(<font face="verdana" size="2" color="#FF0000">Неправильно - не найден $filetocheck, воспользуйтесь кнопкой НАЗАД и исправьте.</font>);
                }
          
        $dirtocheck = "$ikondir" . "data";
        if (-d "$dirtocheck") {
            $datadir = "found"; 
            $makefile = "$ikondir" . "data/test.txt";
            open (TEST, ">$makefile") or $datawritable = "Папка data не записана, проверьте chmod";
            print TEST "-";
            close (TEST);
            $datawritable = "Папка 'data' <b>записана</b>" if (!$datawritable);
            unlink "$makefile";
            } else { $errorflag = "1"; $datadir = "<b>НЕ НАЙДЕНА</b>"; }

        $dirtocheck = "$ikondir" . "help";
        if (-d "$dirtocheck") {
            $helpdir = "found"; 
            $makefile = "$ikondir" . "help/test.txt";
            open (TEST, ">$makefile") or $helpwritable = "Папка 'help' не записана, проверьте chmod";
            print TEST "-";
            close (TEST);
            $helpwritable = "Папка 'help' <b>записана</b>" if (!$helpwritable);
            unlink "$makefile";
            } else { $helpdir = "<b>НЕ НАЙДЕНА</b>"; }

        $dirtocheck = "$ikondir" . "members";
        if (-d "$dirtocheck") {
            $membersdir = "found"; 
            $makefile = "$ikondir" . "members/test.txt";
            open (TEST, ">$makefile") or $memberswritable = "Папка 'members' не записана, проверьте chmod";
            print TEST "-";
            close (TEST);
            $memberswritable = "Папка 'members' <b>записана</b>" if (!$memberswritable);
            unlink "$makefile";
            } else { $errorflag = "1"; $membersdir = "<b>НЕ НАЙДЕНА</b>"; }

        $dirtocheck = "$ikondir" . "messages";
        if (-d "$dirtocheck") {
            $messagesdir = "found"; 
            $makefile = "$ikondir" . "messages/test.txt";
            open (TEST, ">$makefile") or $messageswritable = "Папка 'messages' не записана, проверьте chmod";
            print TEST "-";
            close (TEST);
            $messageswritable = "Папка 'messages' <b>записана</b>" if (!$messageswritable);
            unlink "$makefile";
            } else { $errorflag = "1"; $messagesdir = "<b>НЕ НАЙДЕНА</b>"; }


        $filetocheck = "$imagesdir" . "images/logo.gif";
        if (-e $filetocheck) {
            $found_image = qq(<font face="verdana" size="2" color="#0000FF">Correct</font>);
            }
            else {
                $errorflag = "1"; $found_image = qq(<font face="verdana" size="2" color="#FF0000">Неправильно, воспользуйтесь кнопкой НАЗАД и исправьте.</font>);
                }
          
        $dirtocheck = "$imagesdir" . "images";
        if (-d "$dirtocheck") { $images_dir = "найдена"; } else { $errorflag = "1"; $images_dir = "<b>НЕ НАЙДЕНА</b>"; } 

        $dirtocheck = "$imagesdir" . "emoticons";
        if (-d "$dirtocheck") { $emoticonsdir = "найдена"; } else { $errorflag = "1"; $emoticonsdir = "<b>НЕ НАЙДЕНА</b>"; }

        $dirtocheck = "$imagesdir" . "avatars";
        if (-d "$dirtocheck") { $avatarsdir = "найдена"; } else { $errorflag = "1"; $avatarsdir = "<b>НЕ НАЙДЕНА</b>"; }


        @progs_to_search = ('admincenter.cgi', 'announcements.cgi', 'checkboard.cgi', 'forumoptions.cgi', 'forums.cgi', 'help.cgi', 'ikon.lib', 'ikonadmin.lib',
                            'ikonboard.cgi', 'ikonfriend.cgi', 'ikonmail.lib', 'loginout.cgi', 'messenger.cgi', 'misc.cgi', 'newposts.cgi', 'post.cgi',
                            'postings.cgi', 'printpage.cgi', 'profile.cgi', 'privacy.cgi', 'register.cgi', 'search.cgi', 'setbadwords.cgi', 'setforums.cgi', 'setmembers.cgi',
                            'setmembertitles.cgi', 'setstyles.cgi', 'settemplate.cgi', 'setvariables.cgi', 'topic.cgi', 'viewip.cgi', 'data/progs.cgi', 'data/styles.cgi');

        
		print qq(
		    <font size="5" face="Trebuchet MS" color="#000000">
		    <h1>Помощник установки Ikonboard</b></font></h1>
		    <hr noshade size=1 color="#000000">
		    <br>
		    <font face="verdana" size="3" color="#000000">
		    <b>Добро пожаловать в установку Ikonboard!</b>
		    <br><br><font size=2>
		    <b>Шаг два:</b> Благодарим за ввод сведений. Здесь результаты попытки установки.<br>Если Вы получили данные о любых ошибках, проверьте наличие необходимых папок и файлов на Вашем сервере и правильность установки chmod.</font><br>

		    <hr noshade size=1 color="#000000">
		    <font face="verdana" size="3" color="#0000FF">
		    <b>Правильно ли сохранены введённые данные ?</b></font>
		    <br>
		    $saved_variables
		    <br>
		    <hr noshade size=1 color="#000000">
		    <font face="verdana" size="3" color="#0000FF">
		    <b>Обзор Путей</b></font>
		    <br>
		    <font face="verdana" size="2" color="#000000">
		    Скриптам (*.cgi) Вы выбрали путь: $ikondir - $found_cgi
		    <br><br>
		    -- Просмотр $ikondir data - $datadir - $datawritable<br>
		    -- Просмотр $ikondir help - $helpdir - $helpwritable<br>
		    -- Просмотр $ikondir messages - $messagesdir - $messageswritable<br>
		    -- Просмотр $ikondir members - $membersdir - $memberswritable<br>
		    <br>
		    <br>
		    <font face="verdana" size="2" color="#000000">
		    Для non-cgi (images) Вы выбрали путь: $imagesdir - $found_image
		    <br><br>
		    -- Просмотр $imagesdir images - $images_dir<br>
		    -- Просмотр $imagesdir emoticons - $emoticonsdir<br>
		    -- Просмотр $imagesdir avatars - $avatarsdir<br>

		    <hr noshade size=1 color="#000000">
		    <font face="verdana" size="3" color="#0000FF">
		    <b>Обзор URL</b></font>
		    <br>
		    <font face="verdana" size="2" color="#000000">
		    URL картинок Вы выбрали: $imagesurl
		    <br>
		    <br>
		    -- Просмотр $imagesurl/images/announce.gif - <img src="$imagesurl/images/announce.gif" border=0><br>
		    -- Просмотр $imagesurl/emoticons/smile.gif - <img src="$imagesurl/emoticons/smile.gif" border=0><br>
		    -- Просмотр $imagesurl/avatars/noavatar.gif - <img src="$imagesurl/avatars/noavatar.gif" border=0><br><br>
		    Если у Вас трудности с картинками, проверьте $html_url URL чтобы убедиться в его правильности, также убедитесь,
		    что все картинки загружены на сервер в режиме BINARY.
		    );
		    if ($errorflag eq "1") { print qq(<br><br><font color="#FF0000" size="3"> Помощник установки Ikonboard нашёл ошибки и не может продолжать. Вернитесь и перепроверьте все данные.); print end_html; exit; }

		    
		    print qq(
		    <hr noshade size=1 color="#000000">
		    <font face="verdana" size="3" color="#0000FF">
		    <b>Проверка доступности файлов</b></font>
		    <br>
		    <br>
		    <font face="verdana" size="2" color="#000000">
		    Помощник установки Ikonboard должен проверить *.cgi файлы для уверенности, что все они загружены на сервер в режиме ASCII
		    <br><br>);

		    foreach (@progs_to_search) {

		        $filetotest = "$ikondir" . "$_";
		        if (-e $filetotest) {
		            open (TEST, "$filetotest");
		            @testfile = <TEST>;
			        close (TEST);
			        if (grep(/\r/, @testfile) && $^O ne "MSWin32") {
				        print "Найден $_ который загружен в режиме BINARY. Перезагрузите в ASCII<br>";
		                }
		                else { print "Найден $_ - Загрузка ОК<br>"; }
		            }
		            else { print "<b>Не найден $_ ! - он загружен?</b><br>"; }

		            } # end foreach

		    print qq(
		        <br><br>
		        <hr noshade size=1 color="#000000">
		        <font face="verdana" size="3" color="#0000FF">
		        <b>Конец проверки</b></font>
		        <br>
		        <br>
		        <font face="verdana" size="2" color="#000000">
		        Помощник установки Ikonboard закончил проверку. Если возникают любые ошибки, вернитесь и перепроверьте все данные.
		        <br>Вы можете в любое время изменить введённые сведения в Панели управления Ikonboard.
		        <br><br>
		        Если Вы не уверены в чём-либо, сообщайте в <a href="http://www.ikonboard.com/cgi-bin/ikonboard.cgi"><b>Форум поддержки</b></a>
		        <br><br><i>Конец доклада</i>
		        <br><br>
		        <hr noshade size=1 color="#000000">
		        <font face="verdana" size="3" color="#0000FF">
		        <b>Что Дальше?</b></font>
		        <br>
		        <br>
		        <font face="verdana" size="3" color="#000000">
		        <b>Если Вы только обновляете Ikonboard с младшей версии, <a href="admincenter.cgi?action=remove">ИДИТЕ В ЦЕНТР УПРАВЛЕНИЯ СЕЙЧАС!</a></b>.
		        <font size=2><br>Для лучшей защиты ЭТОТ ФАЙЛ БУДЕТ УДАЛЁН С ВАШЕГО СЕРВЕРА как только Вы выберите переход в Центр управления.<br>
		        Центр управления не запустится, если Вы оставите install.cgi на Вашем сервере! Если автоматическое удаление не срабатывает, удалите install.cgi вручную, через FTP.
		        <br><br>
		        <font size="3"><b>Если это первая установка <a href="$thisprog?action=step_three">ПЕРЕЙДИТЕ К ШАГУ ТРИ!</a></b></font>
		        <br><br><br><br><br>
		        );

                }


elsif ($action eq "step_three") {

    print qq(
    <font size="5" face="Trebuchet MS" color="#000000">
    <h1>Помощник установки Ikonboard</b></font></h1>
    <hr noshade size=1 color="#000000">
     <br>
    <font face="verdana" size="3" color="#FF0000">
    <b>Вы уже побывали здесь?</b>
    <br><br>
    <font face="verdana" size="2" color="#000000">
    <b>Если Вы только обновляете Ikonboard с младшей версии, <a href="admincenter.cgi?action=remove">ИДИТЕ В ЦЕНТР УПРАВЛЕНИЯ СЕЙЧАС!</a></b>.
    <br><br>Если Вы продолжаете установку, статистика Вашей Доски <b>БУДЕТ потеряна</b>! 
    <hr noshade size=1 color="#000000">
    <br><br><font size=2>
    <b>Шаг три:</b><br>
    Окончание установки. Когда эта часть будет завершена, Вы должны будете готовы перейти в Центр управления
    для настройки цветов и оформления общего вида форумов.
    <br>
    <hr noshade size=1 color="#000000">
    <br>
    <font face="verdana" size="3" color="#0000FF">
    <b>Зарегистрируйтесь как администратор.</b></font>
    <br><br>
    <font face="verdana" size="2" color="#000000">
    Сейчас Вы должны зарегистрироваться как администратор. Это позволит Вам входить в Центр управления.</font>
    <br><br>
    <form action="$thisprog" method="post">
    <input type="hidden" name="action" value="final_step">
    <font face="verdana" size="2" color="#000000">
    Выберите себе имя<br>
    <input type="text" name="membername">
    <br><br>
    Выберите пароль<br>
    <input type="password" name="password_one">
    <br><br>
    Повторите ввод пароля<br>
    <input type="password" name="password_two">
    <br><br>
    <input type="submit" value="submit">
    </form>
    <hr noshade size=1 color="#000000">
    <br>
    <b>Дважды проверьте все данные.</b>
    <br><br>);

    } # end step 3

elsif ($action eq "final_step") {

		$namecookie = cookie(-name    =>   "adminname",
		                     -value   =>   "$membername",
		                     -expires =>   "+1d");

		$passcookie = cookie(-name    =>   "adminpass",
		                     -value   =>   "$password_one",
		                     -expires =>   "+1d");

		print header(-cookie=>[$namecookie, $passcookie]); print start_html(-title=>"Помощник установки Ikonboard", -bgcolor=>"#EEEEEE", -style=>{-code=>$stylesheet});

		print qq(
		<font size="5" face="Trebuchet MS" color="#000000">
		<h1>Помощник установки Ikonboard</b></font></h1>
		<hr noshade size=1 color="#000000">
		<br>
		<font face="verdana" size="3" color="#000000">
		<b>Добро пожаловать в установку Ikonboard!</b>
		<br><br><font size=2>
		<b>Последний Шаг:</b><br>
		Помощник установки Ikonboard сейчас создаст административный аккаунт (учётную запись).
		<br>
		<hr noshade size=1 color="#000000">
		<br>
		);

		eval { ($0 =~ m,(.*)/[^/]+,)   && unshift (@INC, "$1"); ($0 =~ m,(.*)\\[^\\]+,) && unshift (@INC, "$1");
		require "data/boardinfo.cgi";
     };
     if ($@) {
     print header('text/html; charset=windows-1251'); print start_html(-title=>"Ошибка Ikonboard!");
     print "Невозможно найти следующие файлы: $@\nЕсли Вы работаете под NT то Вам может понадобиться ввести полный путь в заголовке каждого скрипта";
     print end_html; exit;
     }

		$currenttime = time;
		$blanks = "yes" if (!$membername);
		$blanks = "yes" if (!$password_one);
		$blanks = "yes" if (!$password_two);

		if ($blanks) { print qq(<br><br><font color="#FF0000" size="3"> Пожалуйста, заполните форму полностью, Используйте кнопку НАЗАД, чтобы исправить этот шаг.); print end_html; exit; }
		if ($password_one ne $password_two)  { print qq(<br><br><font color="#FF0000" size="3">Пароли, которые Вы ввели, не согласовываются. Вернитесь назад для исправления этой ошибки.); print end_html; exit; }

		$memberfilename = $membername;
		$memberfilename =~ y/ /_/;
		$membersdir = "$ikondir" . "members";

		$filetomake = "$ikondir" . "members/$memberfilename.cgi";

		open (ADMIN, ">$filetomake") or die "Невозможно открыть файл $filetomake, проверьте пути!";
		print ADMIN "$membername|$password_one|Administrator|ad|0|$adminemail_in|no|private||||||$currenttime||";
		close (ADMIN);

		if (-e $filetomake) {
		print qq(
		<font face="verdana" size="2" color="#000000">
		<b>Поздравляем, Ваша Ikonboard установлена!.</b>
		<br><br>
		Сейчас Вы можете <a href="admincenter.cgi?action=remove">Перейти в Центр управления</a>, настроить форумы и выбрать оформление<br>. Этот Помощник установки должен быть удалён ДО перехода в Центр управления. Оставлять его на Вашем сервере ОГРОМНЫЙ риск!<br>);
		}
		else {
        print qq(
		<font face="verdana" size="2" color="#FF0000">
		<b>Ошибка! Я не могу создать файл Администратора!</b>
		<br><br>
		Проверьте наличие здесь папки 'members': $membersdir );
		}

      $filetomake = "$ikondir" . "data/boardstats.cgi";
        
        
        
       open(FILE, ">$filetomake");
       flock(FILE, 2);
       print FILE "\$lastregisteredmember = \"$membername\"\;\n";
       print FILE "\$totalmembers = \"1\"\;\n";
       print FILE "\$totalthreads = \"0\"\;\n";
       print FILE "\$totalposts = \"0\"\;\n";
       print FILE "\n1\;";
       close (FILE);

		print qq(
		<br><br>
		<hr noshade size=1 color="#000000">
		<font face="verdana" size="3" color="#0000FF">
		Благодарим за использование Ikonboard!</font>
		<br><br>
		<font face="verdana" size="2" color="#000000">
		Мы надеемся, что использование Помощника установки Ikonboard помогло Вам.<br>
		Если у Вас есть другие вопросы, посетите наш <a href="http://www.ikonboard.com/cgi-bin/ikonboard.cgi"><b>Форум Поддержки</b></a>
		<br><br>
		Успехов, <br>
		<i>Команда Ikonboard</i>
		<br><br>
		);

		} # end final step   
    

            else {

				eval '$home = (getpwuid($<))[7];'; if (!-e "C:/") { $pwd = `pwd`; chop $pwd; } if (!eval 'use Cwd;') { eval '$cwd = cwd();'; } else { $cwd = ""; } $prog = $0;
				if ($prog =~ m|install\.(\w+)|) { $prog = "install.$1"; $cgi_extension = $1; } 
				$b4 = $`; $b4 =~ s/\/$//; $b4 =~ s/\\$//; $document_root = $ENV{'DOCUMENT_ROOT'}; $document_root =~ s/\/$//;
				$document_root =~ s/\\$//; $filename = $ENV{'SCRIPT_FILENAME'}; $filename =~ s/\/$prog//; $filename =~ s/\\$prog//;
				$path = $ENV{'PATH_TRANSLATED'}; $path =~ s/\/$//; $path =~ s/\\$//;
				&check($pwd); &check($b4); &check($home); &check($document_root); &check($filename); &check($path); &check($cwd);
				opendir(CURDIR, ".."); while ($q = readdir(CURDIR)) { push (@founddir, $q); }
				closedir(CURDIR); $true_path =~ s%\\%/%g; $true_path =~ s%//%/%g;
				if ($true_path =~ m|(.*)/(.+)|) { $base = $1; $cgi = $2; } else { $base = $true_path; $cgi = "cgi-bin"; }
				$poss_html_dir = "public_html htdocs"; $unsure_html_dir = "htdoc html www wwwdoc wwwdocs wwwroot httpd doc docs"; @poss = split(/\s/, $poss_html_dir);
				@founddir = grep(!/\./, @founddir); $checker = 0;
				foreach $test_dir (@poss) { if (grep(/^$test_dir$/, @founddir)) { $html_dir = "$base/$test_dir/ikonboard"; $checker = 1; last; } }
				if ($checker == 0) { @poss = split(/\s/, $unsure_html_dir); foreach $test_dir (@poss) {
				if (grep(/^$test_dir$/, @founddir)) { if (-e "$base/$test_dir/index.html" || -e "$base/$test_dir/index.htm" || -e "$base/$test_dir/index.php" || -e "$base/$test_dir/index.php3") {
				$html_dir = "$base/$test_dir/ikonboard"; if (-e "$base/$test_dir/index.html" || -e "$base/$test_dir/index.htm" || -e "$base/$test_dir/index.php" || -e "$base/$test_dir/index.php3") {
				$checker = 2; $test_dir_me = $test_dir; last; } else { $checker = 1; last; }
				} else { if (-e "$base/$test_dir/index.html" || -e "$base/$test_dir/index.htm" || -e "$base/$test_dir/index.php" || -e "$base/$test_dir/index.php3") {
				$html_dir = "$base/$test_dir/ikonboard"; $checker = 2; $test_dir_me = $test_dir; last; } else { $checker = 1; last; } } } } }
				if ($html_dir eq "") { $html_dir = "$base/ikonboard"; } $script_dir = "$true_path/ikonboard"; $test_ss = "";
				if ($ENV{'SCRIPT_URI'} ne "") { $test_ss = $ENV{'SCRIPT_URI'}; } elsif ($ENV{'SCRIPT_URL'} ne "") { $test_ss = $ENV{'SCRIPT_URL'};
				} elsif ($ENV{'REQUEST_URI'}) { $test_ss = $ENV{'REQUEST_URI'}; } elsif ($ENV{'SCRIPT_NAME'} ne "") { $test_ss = $ENV{'SCRIPT_NAME'}; }
				if ($test_ss ne "") { if ($test_ss =~ m|^http://([^/]+)|) { $test_ss = $'; } if ($test_ss =~ m|/$prog|) { $test_ss = $`; }
				if ($test_ss ne "") { $script_url = "http://$ENV{'HTTP_HOST'}$test_ss/ikonboard"; }
				} else { $script_url = "http://$ENV{'HTTP_HOST'}/$cgi/ikonboard"; }
				if ($script_url =~ m|^http://([^/]+)/~([^/]+)/|) { $uinfo = "~" . $2 . "/"; }
				$html_url = "http://$ENV{'HTTP_HOST'}/$uinfo" . "ikonboard"; $html_dir =~ s%/%\\%g if $html_dir =~ m|^(\w+):|; $script_dir =~ s%/%\\%g if $script_dir =~ m|^(\w+):|;
				$bdcgi = "$base/$cgi"; $html_dir =~ s%\\\\%\\%g; $script_dir =~ s%\\\\%\\%g; $bdcgi =~ s%\\\\%\\%g;
				if (-e "C:/" || $^O eq "MSWin32") { $OS_USED = 'NT'; }
				$adminemail_in = "incoming\@yourdomain.com"; $adminemail_out = "outgoing\@yourdomain.com";
				$timezone_choice = "<select name=\"timezone\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\" selected>0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
				$time_is_now = localtime; $website_url = "http://$ENV{'HTTP_HOST'}";
				
                    print qq~
				    <form action="$thisprog" method="post">
				    <input type="hidden" name="action" value="step_two">
				    <font size="5" face="Trebuchet MS" color="#000000">
				    <h1>Помoщник установки Ikonboard</b></font></h1>
				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>Добро пожаловать в установку Ikonboard!</b>
				    <br><br><font size=2>
				    <b>Шаг один:</b> Потратьте несколько минут на чтение инструкции и проверки данных перед отправкой этой формы.<br>
				    После отправки этой формы Помощник установки проверит все введённые данные
				    и даст Вам знать, если что-то окажется неверным.<br><br>
				    <b>Перед выполнением этой программы убедитесь, что все файла загружены правильно
				    и имеют необходимые установки CHMOD.</b><br><br>
				    Все введённые здесь сведения могут быть изменены через Центр управления. Как обладатель тайных 
				    возможностей, этот скрипт install.cgi обязан быть удалён после полного выполнения установки. Если Вам понадобится, Вы сможете
				    ещё раз загрузить его на сервер и выполнить установку сначала.</font><br>

				    <hr noshade size=1 color="#000000">

				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>В какой Операционной Системе будет работать IkonBoard?</b><br><br>
				    <font face="verdana" size="2" color="#000000">
				    Выберите что-то одно
				    <br>
				    <br>
				    <select name="OS_USED">
				    <option value="NT" >NT
				    <option value="Unix" selected>Unix
				    </select>

				    <br>
				    <br>
				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>Где находятся файлы на Вашем сервере?</b><br><br>
				    Следующие параметры настройки - только наше лучшее предположение. <font color="#FF0000"><br>Дважды проверьте все настройки и, если что-либо непонятно,
				    спросите об этом на Вашем Веб-хосте.</font><br><br>
				    <font color="#FF0000">Если у Вас NT сервер, используйте двойные обратные черты! ('например: c:\\path\\to\\ikonboard\\')
				    <br><font color="#000000"><b>ПОСТАВЬТЕ '/' (слэш) в конце всех путей</b>
				    <br><br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Где будут установленны *.cgi скрипты?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Это должен быть 'path', a не URL. Он <b>не</b> может начинаться с 'http://'.<br>
				    Это место должно содержать все *.cgi скрипты, которые поставлены с Ikonboard. Следующие
				    папки <b>должны</b> уже быть созданы и содержать в себе необходимые файлы.
				    <ul>
				    <li>data
				    <li>messages
				    <li>messages
				    <li>help
				    </ul><br>
				    <input type="text" size="70" name="ikondir" value="$script_dir/">
				    
				    <br><br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Где находятся картинки?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Это должен быть 'path', a не URL. Он <b>не</b> может начинаться с 'http://'.<br>
				    Это место должно содержать все картинки, которые поставлены с Ikonboard. Следующие
				    папки <b>должны</b> уже быть созданы и содержать в себе необходимые файлы.
				    <br>
				    <b>Не добавляйте '/images/' в конец этого описания!</b>
				    
				    <ul>
				    <li>images
				    <li>emoticons
				    <li>avatars
				    </ul><br>
				    <input type="text" size="70" name="imagesdir" value="$html_dir/">
				    <br>

				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>Каков URL Вашего Веб-сайта?</b><br><br>
				    Следующие параметры настройки - только наше лучшее предположение. <font color="#FF0000"><br>Дважды проверьте все настройки и, если что-либо непонятно,
				    спросите об этом на Вашем Веб-хосте.</font><br><br>
				    <b>Не ставьте '/' (слэш) на конце всех URL</b>
				    <br><br>

				    <font face="verdana" size="3" color="#0000FF">
				    <b>Где расположены картинки?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Это должен быть'URL'. Он <b>должен</b> начинаться с 'http://'.<br>
				    Это место должно содержать все картинки, которые поставлены с Ikonboard.
				    <br> 
				    <br><br>
				    <input type="text" size="70" name="imagesurl" value="$html_url">
				    <br><br>
				    
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Где расположен Ваш сайт?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Это должен быть'URL'. Он <b>должен</b> начинаться с 'http://'.<br>
				    Это должнен быть адрес, который Вы набираете в браузере, чтобы зайти на свой Веб-сайт.
				    <br><br>
				    <input type="text" size="70" name="homeurl" value="$website_url">

				    <br><br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Где расположена Ваша Ikonboard?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Это должен быть'URL'. Он <b>должен</b>  начинаться с 'http://'.<br>
				    <b>НЕ добавляйте 'ikonboard.cgi' в конец. Это URL папки, а не файла</b>.
				    <br><br>
				    <input type="text" size="70" name="boardurl" value="$script_url">

				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>Аватары и смайлики</b><br><br>
				    <font face="verdana" size="2" color="#000000">
				    Аватары - это картинки, которыми пользователи могут обозначать себя в сообщениях.<br>
				    Смайлики преобразуются в графику ,например  ':)'
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Хотите включить аватаров?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Выберите
				    <br><br>
				    <select name="avatars">
				    <option value="on" selected>вкл
				    <option value="off">выкл
				    </select>

				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Хотите включить смайлики?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Выберите
				    <br><br>
				    <select name="emoticons">
				    <option value="on" selected>вкл
				    <option value="off">выкл
				    </select>

				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>E-mail</b><br><br>
				    Следующие параметры настройки - только наше лучшее предположение. <font color="#FF0000">Дважды проверьте все настройки и, если что-либо непонятно,
				    спросите об этом на Вашем Веб-хосте.</font>
				    
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Хотите включить функцию e-mail?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Если Вам не нужно включение функции e-mail, выберите 'ВЫКЛ'
				    и пропустите эту часть раздела.
				    <br><br>
				    <select name="emailfunctions">
				    <option value="off">ВЫКЛ ФУНКЦИИ E-MAIL
				    <option value="on" selected>ВКЛ ФУНКЦИИ E-MAIL
				    </select>
				    <br><br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Какой почтовый протокол будет использоваться?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Выберите протокол и введите путь
				    <br><br>
				    <select name="emailtype">
				    <option value="smtp_mail" selected>SMTP
				    <option value="send_mail">Sendmail
				    <option value="blat_mail">Blat
				    </select>
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>SMTP сервер (если выбрано)</b></font><br><br>
				    <input type=text size="60" name="SMTP_SERVER" value="localhost">
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Путь к Sendmail (если выбрано)</b></font><br><br>
				    <input type=text size="60" name="SEND_MAIL" value="/usr/lib/sendmail">
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Входящий e-mail</b></font><br><br>
				    <input type=text size="60" name="adminemail_in" value="$adminemail_in">
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Исходящий e-mail</b></font><br><br>
				    <input type=text size="60" name="adminemail_out" value="$adminemail_out">
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Вы хотите сделать, чтобы Пользователи получали свой пароль через email, посланный с Ikonboard?</b></font><br>
				    <br>
				    <br>
				    <select name="passwordverification">
				    <option value="no">НЕТ
				    <option value="yes" selected>ДА
				    </select>

				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>Пустячки</b><br><br>
				    <font size=2>Здесь несколько мелочей Вашей Ikonboard.</font>
				    <br>
				    
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Название Вашей Ikonboard</b></font><br>
				    <input type=text size="60" name="boardname" value="My Ikonboard">
				    <br>

				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Описание Вашей Ikonboard</b></font><br>
				    <input type=text size="60" name="boarddescription" value="My Ikonboard for community building">
				    <br>

              <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Ваш копирайт</b><br>Не надо добавлять '&copy\;' - скрипт сделает это сам.<br>
				    &copy\;</font><input type=text size="100" name="copyrightinfo" value="2000 My Website.com">
				    <br>

				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Название сайта</b></font><br>
				    <input type=text size="60" name="homename" value="ikondiscussion.com">
				    <br>

				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Хотите включить защиту от СПАМа?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Защита от СПАМа заставит Ваших Пользователей ожидать определённый промежуток времени, в течении которого они не смогут послать сообщение. Это не влияет на Администраторов или пользователей, которых Вы выдвигаете на статус Модератора.
				    <br>
				    <br>
				    <select name="floodcontrol">
				    <option value="off">ВЫКЛЮЧИТЬ ЗАЩИТУ ОТ СПАМА
				    <option value="on" selected>ВКЛЮЧИТЬ ЗАЩИТУ ОТ СПАМА
				    </select>
				    <br>
				    
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Количество секунд для защиты от СПАМа (если выбрана защита от СПАМа)</b></font><br>
				    <input type=text size=10 name="floodcontrollimit" value="30"> &nbsp; секунд
				    <br>

				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Основной часовой пояс</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Временем Вашего сервера выбрано $time_is_now. Если это неверно, воспользуйтесь окошком для исправления основного времени сервера. 
				    <br>
				    <br>
				    $timezone_choice
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Какое у Вас время?</b></font><br><br>
				    <input type=text size="60" name="basetimes" value="GMT (UK)">
				    <br>

				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>Вам нужен заглавный форум для объявлений?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    Он позволяет Вам, как Администратору,
				    делать общие объявления для всех.
				    <br>
				    <br>
				    <select name="announcements">
				    <option value="no">НЕТ
				    <option value="yes" selected>ДА
				    </select>
				    <br>

				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>Дважды всё проверьте</b><br><br>
				    </font>
				    <br>
				    
				    <input type=submit value=submit>
				    </form>~;
				    }
    print end_html;
    exit(0);

sub check { local ($dr) = @_; return 0 if $dr eq ""; if (-e "$dr/$prog") { $true_path = $dr; return 1; } }

