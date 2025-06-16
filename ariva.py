from colorama import Fore, Style
from time import sleep, time
from os import system
from sms import SendSms
import threading
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.theme import Theme
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, SpinnerColumn
from rich import box
from rich.live import Live
from datetime import datetime
import sys
import logging

logging.basicConfig(filename='bansheenizmsms.log', level=logging.INFO, format='%(asctime)s - %(message)s')

custom_theme_dark = Theme({
    "title": "bold #FFD700 on black",
    "info": "italic cyan",
    "warning": "bold red on black",
    "success": "bold green",
    "prompt": "bold magenta",
    "input": "cyan",
    "border": "#FFD700",
    "gradient1": "bold #FFD700",
    "gradient2": "bold #FFFF00",
    "gradient3": "bold #FF4500"
})

custom_theme_light = Theme({
    "title": "bold #FFD700 on white",
    "info": "italic blue",
    "warning": "bold red on white",
    "success": "bold green",
    "prompt": "bold purple",
    "input": "blue",
    "border": "#FFD700",
    "gradient1": "bold #FFD700",
    "gradient2": "bold #FFFF00",
    "gradient3": "bold #FF4500"
})

current_theme = "dark"
console = Console(theme=custom_theme_dark)

ARIVA_BANNER = """
   ╔══════════════════════════════════════╗
   ║       ✨ PASHA SMS SYSTEM ✨    ║
   ║       Developer By Pasha          ║
   ║   Channel: t.me/millisanalteskilat ║
   ╚══════════════════════════════════════╝
"""

servisler_sms = []
for attribute in dir(SendSms):
    attribute_value = getattr(SendSms, attribute)
    if callable(attribute_value) and not attribute.startswith('__'):
        servisler_sms.append(attribute)

total_sms_sent = 0
show_help = False

def welcome_animation():
    console.clear()
    banner_text = ARIVA_BANNER
    for i in range(len(banner_text) + 1):
        console.print(Text(banner_text[:i], style="gradient1"), end="")
        sys.stdout.flush()
        sleep(0.02)
    console.print()
    console.print(Panel(
        Text("Eğitim amaçlıdır. Kötüye kullanımdan kullanıcı sorumludur.", style="warning", justify="center"),
        border_style="red",
        box=box.ROUNDED
    ))
    sleep(1)

def print_header():
    global total_sms_sent
    console.clear()
    clock = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = Text.assemble(
        (ARIVA_BANNER, "gradient1"),
        (f"\nSistem Saati: {clock}\n", "info"),
        (f"Toplam Gönderilen SMS: {total_sms_sent}\n", "success"),
        ("Eğitim amaçlıdır. Kötüye kullanımdan kullanıcı sorumludur.\n", "warning")
    )
    console.print(Panel(
        header,
        border_style="border",
        box=box.DOUBLE,
        padding=(1, 2),
        title=Text("Bansheenizm", style="gradient2"),
        title_align="left"
    ))

    table = Table(show_header=False, box=box.MINIMAL, style="info")
    table.add_column(style="gradient3")
    table.add_column(style="cyan")
    table.add_row("Servis Sayısı", f"{len(servisler_sms)}")
    table.add_row("Geliştirici", "@Bansheenizm")
    table.add_row("Tema", current_theme.capitalize())
    console.print(table)
    console.print()

def toggle_theme():
    global console, current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
    console = Console(theme=custom_theme_light if current_theme == "light" else custom_theme_dark)
    console.clear()
    print_header()
    console.print(Panel(
        Text(f"Tema {current_theme.capitalize()} olarak değiştirildi!", style="success"),
        border_style="green",
        box=box.ROUNDED
    ))
    sleep(1)

welcome_animation()

while True:
    print_header()
    if show_help:
        help_text = Text.assemble(
            ("Kısayollar:\n", "info"),
            ("[1] Normal SMS Gönderimi\n", "gradient1"),
            ("[2] Turbo SMS Gönderimi\n", "gradient2"),
            ("[3] Çıkış\n", "gradient3"),
            ("[T] Tema Değiştir\n", "info"),
            ("[H] Yardım Menüsünü Gizle/Göster\n", "info")
        )
        console.print(Panel(
            help_text,
            title=Text("Bansheenizm Kısayollar", style="prompt"),
            border_style="border",
            box=box.MINIMAL,
            padding=(1, 2)
        ))

    menu_content = Text.assemble(
        ("1- SMS Gönder (Normal)\n", "gradient1"),
        ("2- SMS Gönder (Turbo)\n", "gradient2"),
        ("3- Çıkış\n", "gradient3"),
        ("[T] Tema Değiştir\n", "info"),
        ("[H] Yardım Menüsünü Göster/Gizle", "info")
    )
    console.print(Panel(
        menu_content,
        title=Text("Bansheenizm Sms Menü", style="prompt"),
        border_style="border",
        box=box.ROUNDED,
        padding=(1, 4)
    ))

    try:
        choice = Prompt.ask(
            Text("Seçim (1-3, T veya H)", style="prompt"),
            choices=["1", "2", "3", "t", "T", "h", "H"],
            default="1",
            show_choices=False
        )
        if choice.lower() == "t":
            toggle_theme()
            continue
        if choice.lower() == "h":
            show_help = not show_help
            continue
        menu = int(choice)
    except ValueError as e:
        error_msg = "Hatalı giriş! Bansheenizm geçerli bir seçim bekliyor."
        console.print(Panel(
            Text(error_msg, style="warning"),
            border_style="red",
            box=box.SQUARE
        ))
        logging.error(f"ValueError: {str(e)} - {error_msg}")
        sleep(3)
        continue

    if menu == 1:
        console.clear()
        print_header()
        tel_no = Prompt.ask(
            Text("Telefon numarasını '+90' olmadan giriniz (Birden çoksa enter)", style="prompt"),
            default=""
        )
        tel_liste = []

        if tel_no == "":
            dizin = Prompt.ask(
                Text("Telefon numaralarının olduğu dosya dizini", style="prompt")
            )
            try:
                with open(dizin, "r", encoding="utf-8") as f:
                    for i in f.read().strip().split("\n"):
                        if len(i) == 10:
                            tel_liste.append(i)
                sonsuz = ""
            except FileNotFoundError as e:
                error_msg = "Hatalı dosya dizini! Ariva Elite doğru bir dizin bekliyor."
                console.print(Panel(
                    Text(error_msg, style="warning"),
                    border_style="red",
                    box=box.SQUARE
                ))
                logging.error(f"FileNotFoundError: {str(e)} - {error_msg}")
                sleep(3)
                continue
        else:
            try:
                int(tel_no)
                if len(tel_no) != 10:
                    raise ValueError
                tel_liste.append(tel_no)
                sonsuz = "(Sonsuz için enter)"
            except ValueError as e:
                error_msg = "Hatalı telefon numarası! Bansheenizm geçerli bir numara bekliyor."
                console.print(Panel(
                    Text(error_msg, style="warning"),
                    border_style="red",
                    box=box.SQUARE
                ))
                logging.error(f"ValueError: {str(e)} - {error_msg}")
                sleep(3)
                continue

        console.clear()
        print_header()
        try:
            mail = Prompt.ask(
                Text("Mail adresi (Bilmiyorsanız enter)", style="prompt"),
                default=""
            )
            if mail and ("@" not in mail or ".com" not in mail):
                raise ValueError
        except ValueError as e:
            error_msg = "Hatalı mail adresi! Bansheenizm geçerli bir mail bekliyor."
            console.print(Panel(
                Text(error_msg, style="warning"),
                border_style="red",
                box=box.SQUARE
            ))
            logging.error(f"ValueError: {str(e)} - {error_msg}")
            sleep(3)
            continue

        console.clear()
        print_header()
        try:
            kere = Prompt.ask(
                Text(f"Kaç SMS göndermek istiyorsunuz {sonsuz}", style="prompt"),
                default=""
            )
            kere = int(kere) if kere else None
        except ValueError as e:
            error_msg = "Hatalı giriş! Bansheenizm sayısal bir değer bekliyor."
            console.print(Panel(
                Text(error_msg, style="warning"),
                border_style="red",
                box=box.SQUARE
            ))
            logging.error(f"ValueError: {str(e)} - {error_msg}")
            sleep(3)
            continue

        console.clear()
        print_header()
        try:
            aralik = int(Prompt.ask(
                Text("Kaç saniye aralıkla göndermek istiyorsunuz", style="prompt")
            ))
        except ValueError as e:
            error_msg = "Hatalı giriş! Bansheenizm sayısal bir değer bekliyor."
            console.print(Panel(
                Text(error_msg, style="warning"),
                border_style="red",
                box=box.SQUARE
            ))
            logging.error(f"ValueError: {str(e)} - {error_msg}")
            sleep(3)
            continue

        console.clear()
        print_header()
        if kere is None:
            sms = SendSms(tel_no, mail)
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}", style="success"),
                BarColumn(bar_width=None, style="green"),
                TimeElapsedColumn(),
                console=console
            ) as progress:
                task = progress.add_task("Bansheenizm SMS Gönderimi", total=None)
                while True:
                    for attribute in servisler_sms:
                        try:
                            exec(f"sms.{attribute}()")
                            progress.update(task, advance=1, description=f"Bansheenizm: {attribute} gönderildi")
                            total_sms_sent += 1
                            logging.info(f"SMS sent: {attribute} to {tel_no}")
                            sleep(aralik)
                        except Exception as e:
                            error_msg = f"Hata: {attribute} gönderilemedi - {str(e)}"
                            console.print(Panel(
                                Text(error_msg, style="warning"),
                                border_style="red",
                                box=box.SQUARE
                            ))
                            logging.error(f"Exception: {str(e)} - {error_msg}")
        else:
            for i in tel_liste:
                sms = SendSms(i, mail)
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}", style="success"),
                    BarColumn(bar_width=None, style="green"),
                    TextColumn("[progress.percentage]{task.completed}/{task.total}"),
                    TimeElapsedColumn(),
                    console=console
                ) as progress:
                    task = progress.add_task("Bansheenizm SMS Gönderimi", total=kere)
                    while sms.adet < kere:
                        for attribute in servisler_sms:
                            if sms.adet == kere:
                                break
                            try:
                                exec(f"sms.{attribute}()")
                                progress.update(task, advance=1, description=f"Bansheenizm: {attribute} gönderildi")
                                total_sms_sent += 1
                                logging.info(f"SMS sent: {attribute} to {i}")
                                sleep(aralik)
                            except Exception as e:
                                error_msg = f"Hata: {attribute} gönderilemedi - {str(e)}"
                                console.print(Panel(
                                    Text(error_msg, style="warning"),
                                    border_style="red",
                                    box=box.SQUARE
                                ))
                                logging.error(f"Exception: {str(e)} - {error_msg}")

        console.print(Panel(
            Text("Menüye dönmek için enter tuşuna basınız...", style="warning"),
            border_style="red",
            box=box.SQUARE
        ))
        input()

    elif menu == 3:
        console.clear()
        console.print(Panel(
            Text("Bansheenizm sistemi kapatılıyor...", style="warning"),
            border_style="red",
            box=box.DOUBLE
        ))
        logging.info("System shutdown")
        break

    elif menu == 2:
        console.clear()
        print_header()
        tel_no = Prompt.ask(
            Text("Telefon numarasını '+90' olmadan giriniz", style="prompt")
        )
        try:
            int(tel_no)
            if len(tel_no) != 10:
                raise ValueError
        except ValueError as e:
            error_msg = "Hatalı telefon numarası! Bansheenizm geçerli bir numara bekliyor."
            console.print(Panel(
                Text(error_msg, style="warning"),
                border_style="red",
                box=box.SQUARE
            ))
            logging.error(f"ValueError: {str(e)} - {error_msg}")
            sleep(3)
            continue

        console.clear()
        print_header()
        try:
            mail = Prompt.ask(
                Text("Mail adresi (Bilmiyorsanız enter)", style="prompt"),
                default=""
            )
            if mail and ("@" not in mail or ".com" not in mail):
                raise ValueError
        except ValueError as e:
            error_msg = "Hatalı mail adresi! Ariva Elite geçerli bir mail bekliyor."
            console.print(Panel(
                Text(error_msg, style="warning"),
                border_style="red",
                box=box.SQUARE
            ))
            logging.error(f"ValueError: {str(e)} - {error_msg}")
            sleep(3)
            continue

        console.clear()
        print_header()
        send_sms = SendSms(tel_no, mail)
        dur = threading.Event()

        def Turbo():
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}", style="success"),
                BarColumn(bar_width=None, style="green"),
                TimeElapsedColumn(),
                console=console
            ) as progress:
                task = progress.add_task("Bansheenizm Turbo Gönderim", total=None)
                while not dur.is_set():
                    thread = []
                    for fonk in servisler_sms:
                        try:
                            t = threading.Thread(target=getattr(send_sms, fonk), daemon=True)
                            thread.append(t)
                            t.start()
                            progress.update(task, advance=1, description=f"Bansheenizm Turbo: {fonk} gönderildi")
                            total_sms_sent += 1
                            logging.info(f"Turbo SMS sent: {fonk} to {tel_no}")
                        except Exception as e:
                            error_msg = f"Hata: {fonk} gönderilemedi - {str(e)}"
                            console.print(Panel(
                                Text(error_msg, style="warning"),
                                border_style="red",
                                box=box.SQUARE
                            ))
                            logging.error(f"Exception: {str(e)} - {error_msg}")
                    for t in thread:
                        t.join()

        try:
            Turbo()
        except KeyboardInterrupt:
            dur.set()
            console.clear()
            console.print(Panel(
                Text("Ctrl+C algılandı. Bansheenizm menüye dönüyor...", style="warning"),
                border_style="red",
                box=box.SQUARE
            ))
            logging.info("Turbo mode interrupted")
            sleep(2)
