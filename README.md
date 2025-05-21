# DSA projekts par procesoriem
Iegūt informāciju par labākajiem stacionāro datoru procesoriem un to cenām Latvijā.  
Noteikt, kuri no tiem ir izdevīgākie procesori Latvijā.

## Projekta uzdevumi:
* Nolasīt labāko stacionāro datoru ***(dekstop)*** procesoru sarakstu un to testēšanas rezultātu punktus no [cpu benchmark](https://www.cpubenchmark.net/top-gaming-cpus.html)!
* Katram stacionāro datoru procesoram atrast cenu Latvijā no interneta veikala [dateks](https://www.dateks.lv)!
* Procesoru meklēšanai interneta veikalā izmantot saiti: `https://www.dateks.lv/meklet?q=`
* Nolasīt katra procesora lētāko cenu veikalā!
* Nolasīt katram procesoram saiti uz lapu, kurā to var iegādāties!
* Aprēķināt katram procesoram testēšanas rezultātu punktus uz 1 eiro!
* Ja procesors nav pieejams interneta veikalā, tad `price="Not Found"`, `score/EUR="N/A"` un `link="No link found"`
* Iegūto informāciju saglabāt izklājlapu datnē `cpus.xlsx` (Kolonnu nosaukumi: ***CPU Name, Score, Price(EUR), Score/EUR, Link***)!
* Atfiltrēt nost tos procesorus, kuri nav pieejami interneta veikalā, atstājot tikai tos, kuri ir pieejami!
* Noteikt procesoriem rangu pēc testēšanas rezultātu punktiem!
* Notiekt procesoriem rangu pēc testēšanas rezultātu punktiem uz 1 eiro!
* Noteikt kopējo rangu, kur `total_rank = score_rank + score_per_euro_rank`!
* Sakārtot datus pēc kopējā ranga!
* Ja vairākiem procesoriem ir vienāds kopējais rangs, tad sakārtot tos pēc testēšanas rezultātu punktiem!
* Iegūto informāciju saglabāt izklājlapu datnē `ranked_cpus.xlsx` (Kolonnu nosaukumi: ***CPU Name, Score, Price(EUR), Score/EUR, Link, Score Rank, Score/EUR Rank, Total Rank***)!

## Izmantotās bibliotēkas:
* requests - tīmekļa pieprasījumu veikšanai
* BeautifulSoup - informācijas izgūšanai no tīmekļa lapām
* urllib.parse (quote_plus) - lai pārveidotu simboliskas virknes tīmekļa saišu formātā
* pandas - darbībām ar izklājlapām un informācijas filtrēšanai, kārtošanai
* tqdm - progresa indikatoram
* time - koda izpildes palēlināšanai, lai nepārslogotu tīmekļa serverus
* random - gadījumvērtību iegūšanai, kuras izmantot gaidīšanām, lai simulētu reāla lietotāja pieprasījumus

## Izstrādes metode
Lai projekta atrisināšana kļūtu vienkāršāka sadalīju projektu 2 daļās:
1. Datu iegūšana un `cpus.xlsx` izveide
2. Datu analīze un `ranked_cpus.xlsx` izveide

Katrai daļai izstrādāju savu Python kodu.
* `scraper.py`
* `analyser.py`