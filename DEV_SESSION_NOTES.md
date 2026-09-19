# OpenCPN calisma notlari

## 2026-09-17: Turkce yerel ortam duzeltmesi ve profil onarimi

- Kullanici uygulamayi kapatti; dis ortamda pgrep ile opencpn sureci kalmadigi dogrulandi.
- Linux masaustunde config okunmadan once ve ChangeLocale sonunda LC_CTYPE=C.UTF-8 (alternatif C.utf8) sabitlendi. LC_MESSAGES/Turkce arayuz secimi korunuyor. Android ve diger platformlar degistirilmedi.
- Dosyalar: gui/src/ocpn_app.cpp, gui/src/ocpn_platform.cpp.
- Yeni yedek: build-debug/config-investigation/opencpn-20260917-213913.conf.bak.
- 188 tekrarli anahtar ve tekrarli bolumler aday kopyada birlestirildi. Genel ayarlarda son kayit korundu; Dashboard1 kimligi ve alti alet (0,4,20,2,1,3) onceki ekran goruntusunden geri getirildi; panel boyutu 168x729.
- verify-repair.cpp, wxWidgets 3.2.9 ile GUI acmadan aday dosyayi okudu; assertion yok. Turkce wxLocale gecisi sonrasinda 6 alet, Turkce baslik, UTF-8 dosya adi donusumu ve uc kaydet/oku turu basarili.
- cmake --build build-debug --parallel 2, cmake --install build-debug ve git diff --check basarili.
- Etkin config'in yedekten sonra degismedigi kontrol edilerek aday dosya atomik olarak config-ready/opencpn.conf yerine kondu.
- Uygulama bu duzeltmeden sonra ajan tarafindan acilmadi: kullanici Run -> Start Debugging ile iki acilis/kapanis kontrolu yapacak. Tum Unicode islemleri ve diger platformlar icin kapsamli test yapilmadi; bu yerel Linux duzeltmesidir.

## Dashboard kaybi ve SetLine hatasi: neden incelemesi

- Etkin ayarlar degistirilmeden `build-debug/config-investigation/opencpn-before.conf` yedegi alindi.
- wxWidgets 3.2.9 ile bagimsiz, GUI veya UDP kullanmayan deneme: `build-debug/config-investigation/config-probe.cpp`.
- C yerel ortaminda okunan temiz Dashboard ayarlari, LC_ALL tr_TR.utf8 yapilinca `InstrumentCount=6` degerini bulamiyor. Ardindan Write ayni bolume ikinci `InstrumentCount=0` ekliyor.
- C -> C ve tr_TR.utf8 -> tr_TR.utf8 kontrollerinde okuma basarili (6); tr_TR.utf8 -> C gecisinde de okuma basarisiz.
- Turkceye gecisten sonra LC_CTYPE=C geri yuklenen denemede okuma yeniden basarili. Bu olasi cozum yonudur; uygulamaya uygulanmadi, Unicode/arayuz etkileri incelenmeli.
- Yalnizca iki `[Settings/AIS]` basligi bulunan ayri ornek, ayni `SetLine: changing line for a non-root group?` assertion'unu uretti.
- Gercek dosyada `[Settings/AIS]` uc kez; Dashboard1 icinde InstrumentCount once 6 sonra 0. Son kopyada Instrument1..6 kayitlari yok; onceki kullanici goruntusu degerleri 0,4,20,2,1,3 olarak belgeliyor.
- Kod sirasi: ocpn_app.cpp GetConfigObject/LoadMyConfig ardindan ChangeLocale cagiriyor. ChangeLocale wxLocale::Init ile yerel ortami degistiriyor, sadece LC_NUMERIC'i C'ye geri aliyor. Dashboard daha sonra ayarlari okuyor/yaziyor.
- Sonuc: yerel ortam degisimiyle wxFileConfig anahtar aramasinin bozulmasi bagimsiz olarak kanitlandi; ekrandaki assertion ise tekrarli bolum basliklariyla birebir uretildi. Ilk bozulmanin tarihsel her yazma adimi izlenmis degildir.
- Uygulama kaynaklari veya etkin profil bu incelemede degistirilmedi. Sonraki is: anahtar aramasini dil degisiminden koruyan cozumun yan etkilerini dogrulamak, profil kopyasini tekrarli anahtar/bolumleri birlestirerek onarmak ve Dashboard'u bilinen degerlerle kurtarmak; sonra kullanicinin iki acilis/kapanis testi.

## 2026-09-17: Harita ve NMEA denemesi

- Ayri profil: `build-debug/integration-test/config`; asil F5 profili degistirilmedi.
- OpenCPN sitesinden `https://opencpn.org/OpenCPN/doc/MED.7z` indirildi; `charts/Med01.kap` cikarildi.
- Log, harita verisinin yuklendigini ve chart nesnesinin baslatildigini dogruluyor. Ekranin gorsel dogrulamasi yapilmadi.
- UDP 127.0.0.1:10119 uzerinden `send-gps.py` ile 12 saniye checksum'li RMC/GGA gonderildi. Bu SIMULE veridir.
- Uygulama logu 09:06:30 ve 09:06:34'te konumu 36 N, 25 E olarak dogruladi. Gonderim bitince GPS watchdog timeout beklenen sekilde olustu.
- Messaging.All0183, Position.ParseGGA, uc AIS testi, iki koordinat donusum testi ve N0183Nuffer.Basic gecti (8 test).
- Loopback.N0183 tek basina surucu olusturmadigi icin coktu; `./tests --gtest_filter=Loopback.Exists:Loopback.N0183` birlikte 2/2 gecti.
- NavUtils.ParseGPXDateTime yerel saat diliminde basarisiz, TZ=UTC ile basarili; bu kosul farki acik bulgudur.
- Bu test oturumunda `--quit` pencereyi kapatmadi. Test penceresine normal WM_DELETE_WINDOW gonderme izni kullanici tarafindan reddedildi; pencere acik birakildi. Bu oturumun kapanisi dogrulanmadi.
- Gercek GPS donanimi ve guncel seyir haritasi test edilmedi; indirilen pilot harita sadece yukleme testi icin kullanildi.

## 2026-09-17: Kurulum tamamlandi

- Debug derleme ve yerel kurulum yeniden tamamlandi; eksik dinamik kutuphane yok.
- `config-ready` profili, onceki sihirbazi tamamlanmis audit profilinin ayarlarindan olusturuldu; eski profiller korundu.
- Bos harita listesiyle `-D` acilisi denendi: `OnInitTimer...Last Call` ve `Finalize Canvases` asamalarina ulasti.
- `--quit` ile normal kapanis dogrulandi: uygulama cikis kodu 0, logda `MyApp exiting cleanly`.
- F5 artik `config-ready` kullaniyor. Terminalden `./start-opencpn.sh` ile acilabilir.
- Ilk kullanim sihirbazi bu kontrolde tekrar edilmedi; ayni veritabani yenileme yolu `-D` ile tetiklendi.

Son inceleme: 2026-09-16. Bu not, onceki konusmanin yerine dosyalar,
Git farklari, derleme ayarlari ve mevcut loglardan elde edilen kanitlari kaydeder.
Onceki asil ozellik hedefi bilinmiyor. Tum kaynak kodun eksiksiz hata denetimi
yapilmadi; yerel degisiklikler ve bunlarla ilgili calistirma akisi incelendi.

## Kaldigimiz yer

- HEAD: `91f3b6743` (`Version 5.14.0`).
- Debug derleme dizini: `build-debug`.
- Yerel kurulum: `build-debug/install`.
- VS Code F5 profili: `OpenCPN Debug (GDB)`.
- F5, `build-debug/install/bin/opencpn` dosyasini
  `--configdir build-debug/config-clean` ile baslatir.
- F5 oncesindeki gorev zinciri: configure -> build (2 is) -> install.
- Eski deneme profili: `build-debug/config`; sonraki profil: `config-clean`.
  Ismindeki clean, artik sifir veya sorunsuz profil oldugu anlamina gelmiyor.
- Son mevcut GUI logunda 16:59:42'de baslatma ve OpenGL kurulumu basarili;
  17:00:14'te duzgun kapanis var. Bu incelemede GUI yeniden acilmadi.

## Dosyalar ve mevcut degisiklikler

| Dosya | Durum / amac |
| --- | --- |
| `model/src/plugin_handler.cpp:126` | `glob_dir`, acilamayan dizin icin bos sonuc donduruyor; acilmamis wxDir ile GetFirst cagrilmasini onluyor. |
| `.vscode/settings.json` | Debug dizini, yerel kurulum, compile_commands, 2 paralel is ayarlari eklenmis. |
| `.vscode/c_cpp_properties.json` | Derleyici gcc yerine g++ yapilmis. |
| `.vscode/launch.json` | GDB ve ayri config profili mevcut; Git tarafindan izlenmiyor. |
| `.vscode/tasks.json` | Configure/build/install gorevleri mevcut; Git tarafindan izlenmiyor. |
| `.vscode/extensions.json` | Yerel dosya; Git tarafindan izlenmiyor. |
| `flatpak/org.opencpn.OpenCPN` | Alt modul beklenen `374b200e6` yerine `f6508998a` commit'inde; bu farkin amaci bilinmiyor. |
| `gui/src/ocpn_app.cpp` | Acik editor dosyasi; HEAD'e gore yerel icerik degisikligi yok. Baslatma, tek ornek/IPC ve kapanis burada. |

`.gitignore`, `.vscode` dizinini dislar. Onceden izlenen iki ayar dosyasi
diff'te gorunur, yeni launch/tasks dosyalari gorunmez. Baska checkout'a
aktarilirken F5 kurulumunun kaybolmamasi icin bu dosyalar ayrica ele alinmali.
Alt modul farki ve mevcut kaynak degisiklikleri bu incelemede korunmustur.

## Projede yon bulma

- `gui/src/ocpn_app.cpp`: uygulamanin baslatilmasi ve kapanisi.
- `gui/src/ocpn_frame.cpp`: ana pencere ve gecikmeli baslatma.
- `gui/src/navutil.cpp`: uygulama ayarlarinin okunmasi/yazilmasi.
- `model/src/plugin_handler.cpp`: eklenti kurulum verileri ve import dosyalari.
- `model/src/navmsg_filter.cpp`: mesaj filtrelerinin yuklenmesi.
- `plugins/`: birlikte derlenen eklentiler.
- `test/`: mevcut testler; `test/CMakeLists.txt` test kayitlarini tanimlar.
- `data/`, `libs/`, `CMakeLists.txt`: kaynaklar, kutuphaneler, derleme tanimi.

## Bulgular ve belirsizlikler

1. **Ayar dosyasinda tekrarlar dogrulandi.**
   `build-debug/config-clean/opencpn.log:125` ve devaminda yinelenen anahtar
   uyarilari var. Mevcut `opencpn.conf` icinde `bShowS57Text` ve
   `bShowS57ImportantTextOnly` ayni grupta tekrarlaniyor. ObjectFilter icinde
   `vizDISMAR` / `vizdismar` gibi farkli harf buyuklukleri de var.
   Eski `config` profilinin logunda cok daha fazla tekrar bulunuyor.
   Kaynak noktalar: `gui/src/navutil.cpp:166` (wxFileConfig), `:1286` ve
   `:2105` (ObjectFilter), `:2251` (S57 ayarlari), `:2418` (Flush).
   Kok neden henuz kanitlanmadi; elle duzenleme, onceki denemeler veya
   okuma/yazma davranisi birbirinden ayrilmali. Mevcut profil silinmedi.

2. **Gecmiste IPC baglanti uyarisi var.**
   `config-clean/opencpn.log:106`, 16:58:11'de yerel IPC baglantisi kurulamamis.
   `gui/src/ocpn_app.cpp:750` civarindaki tek-ornek kontrolu bu durumu ele aliyor.
   Daha sonraki basarili acilis nedeniyle halen suren hata oldugu soylenemez.
   Tekrar ederse calisan surecler ve kilit/IPC durumu incelenmeli.

3. **Filtre dizini uyarisi var.**
   Her iki profilin ilk kayitlarinda profil altindaki `filters` yolu icin uyari
   bulunuyor. `model/src/navmsg_filter.cpp:187` civari dizin okuma hatasinda
   bos listeyle devam ediyor. Son oturumda tekrarlandigi dogrulanmadi.

4. **IDE yedek include yollari eski.**
   `.vscode/settings.json` icinde wx-3.0/wx-3.1 ve `build/include` var;
   asil derleme Debug compile_commands kullaniyor. Bu tek basina derleme
   hatasi degil; basliklarda kirmizi cizgi gorulurse CMake provider ve
   compile_commands secimi kontrol edilmeli.

5. **Eklenti dizini korumasinin kapsam siniri.**
   IsOpened kontrolu yerinde gorunuyor; bulunamayan dizinle erisim izni
   sorununu ayni bos sonuc olarak ele aliyor. Bu kontrolun eksik dizin
   senaryosu bu oturumda ayri bir testle yeniden uretilmedi.

## Bu oturumda dogrulananlar

- `git diff --check`: basarili.
- `cmake --build build-debug --parallel 2`: basarili, tum hedefler tamamlandi.
- Asagidaki mevcut test secimi: 12/12 basarili.

```sh
ctest --test-dir build-debug/test -R '^(RoutePointScaleTest\.|Buffer\.|N0183Nuffer\.)' --output-on-failure --timeout 30
```

Tum test paketi, GUI, gercek GPS/NMEA, harita ve ag/IPC entegrasyonlari bu
incelemede calistirilmadi. Basarili 12 test tum uygulamanin hatasizligini
veya plugin_handler degisikliginin dogrulugunu tek basina kanitlamaz.
Bu oturumda `cmake --install` calistirilmadi; F5 bunu otomatik yapar.

## Donuste devam sirasi

1. Mevcut profilleri koruyarak yeni bir deneme profiliyle F5 acilis/kapanis
   denemesi yap. Gerekiyorsa launch argumanini yeni profile yonlendir.
2. Ilk ve ikinci acilis sonrasinda ayar dosyasini ve logunu karsilastir;
   tekrarlar sifirdan olusuyorsa ayar yazma yolunu incele.
3. Yeniden olusan IPC veya filters uyarisi varsa o oturumun loguyla arastir.
4. Launch/tasks dosyalarinin projeyle birlikte tutulmasini degerlendir;
   alt modul farkinin istenen bir guncelleme olup olmadigini netlestir.
5. Ortam dogrulandiktan sonra sonraki islevsel hedefi sec: harita, rota,
   GPS/NMEA denemesi veya belirli bir kaynak kod degisikligi.

2026-09-16 incelemesinin tek elle eklenen dosyasi bu nottur; o incelemede
kod duzeltmesi yapilmadi.

## 2026-09-17: Ilk acilista kapanmama

- Yeni profil: `build-debug/config-audit-20260917-TIQ22y`.
- Kullanici ilk kullanim sihirbazini tamamladi; ana pencere acildi fakat X
  ile kapanmadi. Log `OnInitTimer...0` asamasinda kaldi. Profilde
  `ChartDirectories` grubu bulunmadi.
- Kod akisi: sihirbaz `g_NeedDBUpdate = 2` ayarliyor. OnInitTimer,
  StartRebuildChartDatabase cagrisi sonrasi geri donuyor. Harita dizini yoksa
  bu fonksiyon is baslatmiyor ve init zamanlayicisini yeniden baslatmiyordu.
  `g_bDeferredInitDone` false kaldigindan OnCloseWindow istegi yok sayiyordu.
- `gui/src/ocpn_frame.cpp` icinde bos harita dizini durumunda InitTimer
  yeniden baslatildi. Harita dizini olan durumun callback akisi korundu.
- Derleme, yerel kurulum ve `git diff --check` basarili.
- Eski test sureci SIGTERM'e de yanit vermedi; sadece bu test sureci
  SIGKILL ile kapatildi. Bu, normal kapanis dogrulamasi DEGILDIR.
- Duzeltmeden sonra ilk kullanim sihirbazi + bos harita listesiyle GUI
  yeniden denemesi henuz yapilmadi. Once bu senaryo, ardindan iki normal
  acilis/kapanisla ayar tekrarlarinin kontrolu tamamlanmali.

## 2026-09-17: Harita dizini basligi onarimi

- Kullanici normal kapanis yapti; log 22:15:14 MyApp exiting cleanly, pgrep surec yok ve startcheck.dat yok.
- config-ready/opencpn.conf icinde hatali `""[ChartDirectories]` basligi vardi; log satir 676 icin `= expected` hatasini dogruladi.
- Yedek: build-debug/config-investigation/opencpn-before-chart-header-20260917-221533.conf.bak. Baslik `[ChartDirectories]` olarak duzeltildi; diger ayarlar korundu.
- Med01.kap dosyasi mevcut. Sozdizimi/tekrar kontrolu ve verify-repair (6 gosterge, Turkce/UTF-8, 3 kaydet/oku) basarili.
- Yeniden acilista haritanin gorunmesi henuz kullanici tarafindan dogrulanmadi.

## 2026-09-17: Kullanici yeniden acilis dogrulamasi

- Kullanici haritanin acildigini, sonraki yeniden acilista harita ve Gosterge Panelinin birlikte korundugunu bildirdi.
- Etkin config tekrarli anahtar ve hatali satir kontrolunden gecti; harita dizini basligi duzgun ve InstrumentCount=6.
- Bu gorsel sonuc kullanici bildirimidir; gercek GPS verisi veya tum uygulama testinin dogrulamasi degildir.
