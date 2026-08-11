(function () {
  "use strict";

  const STORAGE_KEY = "ober_lang";
  const lang = localStorage.getItem(STORAGE_KEY) === "ru" ? "ru" : "uz";

  const RU = {
    "OBER bosh sahifa":"Главная OBER",
    "Bosh sahifa":"Главная",
    // Tab bar 2026-08-10 da ISH bo'yicha nomlandi: sahifa nomi emas,
    // odam nima qilayotgani. "Qidirish" — xaridor tomoni.
    "Qidirish":"Поиск",
    "E’lon":"Объявление",
    "+ E’lon":"+ Объявление",
    "Sotish":"Продать",
    "Sotish bo‘limlari":"Разделы продажи",
    "Xaridor so‘rovlari":"Запросы покупателей",
    "Hozir emas":"Не сейчас",
    "Telegram ulangan":"Telegram подключён",
    "Yangi xaridor so‘rovi va chat xabari Telegram orqali keladi.":"Новый запрос покупателя и сообщение в чате придут в Telegram.",
    "Botni ochish":"Открыть бота",
    "Telegram holatini tekshira olmadik.":"Не удалось проверить подключение Telegram.",
    "Kategoriyalar":"Категории",
    "kategoriyalar":"категории",
    "Transport":"Транспорт",
    "Ko'chmas mulk":"Недвижимость",
    "Elektr jihozlari":"Электроника",
    "Uy va bog'":"Дом и сад",
    "Bolalar dunyosi":"Детский мир",
    "Moda va stil":"Мода и стиль",
    "Xizmatlar":"Услуги",
    "Ish":"Работа",
    "Hayvonlar":"Животные",
    "Xobbi va sport":"Хобби и спорт",
    "Tekinga beraman":"Отдам даром",
    "Ayirboshlash":"Обмен",
    "Yangi e'lon":"Новое объявление",
    "Sotuvchi":"Продавец",
    "Profil":"Профиль",
    "Bo'limni tanlang — shu bo'yicha bozordan qidiramiz.":"Выберите раздел — найдём на рынке по этой теме.",
    "Bozor bo'limlari yuklanmoqda…":"Загружаем разделы рынка…",
    "Bo'limlarni hozir yuklay olmadik. Internetni tekshirib, sahifani yangilang.":"Не удалось загрузить разделы. Проверьте интернет и обновите страницу.",
    "Shu bo'limdan qidirish":"Искать в этом разделе",
    "OBER — siz yozasiz, bozor javob beradi":"OBER — вы пишете, рынок отвечает",
    "OBER — sotuvchi kabineti":"OBER — кабинет продавца",
    "OBER — takliflar va xabarlar":"OBER — чат и сообщения",
    "Chat":"Чат",
    "Suhbatni tanlang":"Выберите диалог",
    "Taklifni oching. Narx, rasm va yozishmalar shu yerda ko‘rinadi.":"Откройте предложение. Цена, фото и переписка появятся здесь.",
    "Takliflar":"Предложения",
    "Javoblar":"Ответы",
    "Xabarlar":"Сообщения",
    "Sotuvchimisiz?":"Вы продавец?",
    "Xaridor sahifasi":"Страница покупателя",
    "sotuvchi kabineti":"кабинет продавца",
    "Chiqish":"Выйти",
    "Keraklisi shu yerda":"Всё нужное — здесь",
    "Siz yozasiz. Bozor javob beradi.":"Вы пишете. Рынок отвечает.",
    "OLX, Telegram va OBER e’lonlari — bitta qidiruvda.":"Объявления OLX, Telegram и OBER — в одном поиске.",
    "Hozir bozorda":"Сейчас на рынке",
    "Eng so‘nggi qo‘shilgan e’lonlar":"Последние добавленные объявления",
    "Butun bozorni bir joyda ko‘ring":"Весь рынок в одном месте",
    "Sotuvchilardan javob oling":"Получайте ответы продавцов",
    "Nega OBER?":"Почему OBER?",
    "Barcha manbalar bitta joyda":"Все источники в одном месте",
    "Bir so‘rovda butun bozor":"Весь рынок одним запросом",
    "Bugun bor-yo‘qligini so‘raydi":"Спрашивает, есть ли сегодня",
    "Noto‘g‘ri modelni kesadi":"Отсекает неверные модели",
    "Qidirmaysiz — so‘raysiz":"Не ищете — спрашиваете",
    "Sotuvchilar uchun":"Продавцам",
    "Aloqa":"Контакты",
    "Maxfiylik":"Конфиденциальность",
    "Qoidalar":"Правила",
    "Ochiq bozor — OLX, Telegram va boshqa manbalar bitta qidiruvda.":"Открытый рынок — OLX, Telegram и другие источники в одном поиске.",
    "divan":"диван",
    "kir yuvish mashinasi":"стиральная машина",
    "velosiped":"велосипед",
    "2 xonali kvartira":"2-комнатная квартира",
    "telefon ekrani":"экран телефона",
    "Nima kerakligini yozing":"Напишите, что вам нужно",
    "O‘zbekcha, ruscha, aralash — qanday yozsangiz ham tushunamiz. Ro‘yxatdan o‘tish shart emas.":"Пишите по-узбекски, по-русски или смешанно — поймём в любом виде. Регистрация не нужна.",
    "Har kartada manba ko‘rinadi. Tashqi e’lonni bossangiz, asl havolasi ochiladi.":"На каждой карточке указан источник. Внешнее объявление откроется по исходной ссылке.",
    "Topilmasa, mos sotuvchilardan so‘rang. Chat aloqa uchun; to‘lov va yetkazish OBERda emas.":"Если не нашли, спросите подходящих продавцов. Чат — для связи; оплата и доставка проходят не в OBER.",
    "Masalan: 25 m² banner":"Например: баннер 25 м²",
    "Topish":"Найти",
    "Rasm bilan qidirish":"Поиск по фото",
    "Qidiruv uchun tanlangan rasm":"Выбранное фото для поиска",
    "Rasm tanlandi":"Фото выбрано",
    "Izoh yozishingiz mumkin yoki darhol qidiring":"Добавьте описание или сразу начните поиск",
    "Rasmni olib tashlash":"Удалить фото",
    "Rasm tayyorlanmoqda…":"Подготавливаем фото…",
    "AI rasmni mahsulot qidiruviga aylantiradi.":"ИИ превратит фото в поисковый запрос.",
    "AI rasmni tushunyapti…":"ИИ анализирует фото…",
    "AI tushundi:":"ИИ распознал:",
    "AI hali ulanmagan — yozgan matningiz bo‘yicha qidirdik.":"ИИ ещё не подключён — выполнили поиск по вашему тексту.",
    "Rasmli qidiruvni yakunlab bo‘lmadi":"Не удалось выполнить поиск по фото",
    "Faqat JPG, PNG yoki WEBP rasm tanlang":"Выберите фото JPG, PNG или WEBP",
    "Rasm 8 MB dan kichik bo‘lishi kerak":"Фото должно быть меньше 8 МБ",
    "Rasmni tayyorlab bo‘lmadi":"Не удалось подготовить фото",
    "Qayerdan qidiramiz?":"Где искать?",
    "Viloyat":"Область",
    "Butun O‘zbekiston":"Весь Узбекистан",
    "O‘zbekiston":"Узбекистан",
    "Shahar yoki tuman":"Город или район",
    "Shahar / tuman":"Город / район",
    "Butun viloyat":"Вся область",
    "Viloyatni tanlang":"Выберите область",
    "Kategoriya qidirish…":"Поиск категории…",
    "Kategoriya qidirish":"Поиск категории",
    "Hech narsa topilmadi":"Ничего не найдено",
    "Boshqa so‘z bilan urinib ko‘ring.":"Попробуйте другое слово.",
    "yaqin takliflar tepaga chiqadi":"ближайшие предложения будут выше",
    "yaqin e’lonlar tepaga chiqadi":"ближайшие объявления будут выше",
    "Namuna so‘rovlar":"Примеры запросов",
    "Bozor ma’lumoti yuklanmoqda…":"Загружаем данные рынка…",
    "ta":"",
    "narx ko‘rsatilmagan":"цена не указана",
    "ta ochiq e’lon narxi va jonli sotuvchi javoblari":"цен открытых объявлений и живых ответов продавцов",
    "Ochiq e’lon narxlari va jonli sotuvchi javoblari":"Цены открытых объявлений и живые ответы продавцов",
    "Natijalar yuklanmoqda":"Результаты загружаются",
    "Qidiruvni hozir yakunlay olmadik. Iltimos, bir ozdan keyin qayta urinib ko‘ring.":"Не удалось завершить поиск. Пожалуйста, попробуйте ещё раз чуть позже.",
    "Qidiruvga ulanib bo‘lmadi":"Не удалось подключиться к поиску",
    "Internetni tekshirib, shu so‘rovni yana bir marta yuboring.":"Проверьте интернет и отправьте этот запрос ещё раз.",
    "Qayta urinish":"Повторить",
    "Narxlar taqsimoti":"Распределение цен",
    "Jonli qidiruv":"Живой запрос",
    "Bugungi holat":"Актуально сегодня",
    "Sotuvchilardan bevosita so‘raymiz":"Спросим продавцов напрямую",
    "Aniq bormi? Bir so‘rov bilan biling.":"Есть ли в наличии? Узнайте одним запросом.",
    "So‘rov mos sotuvchilarga OBER ichida boradi. Javob: bor-yo‘qligi va narxi.":"Запрос попадёт подходящим продавцам внутри OBER. В ответе — наличие и цена.",
    "Nima kerak?":"Что вам нужно?",
    "Byudjet":"Бюджет",
    "Telefon raqami":"Номер телефона",
    "Yuborish":"Отправить",
    "Telefon raqamingiz sotuvchiga ochilmaydi; u akkaunt va OBER bildirishnomalari uchun.":"Продавец не увидит ваш номер; он нужен для аккаунта и уведомлений OBER.",
    "Nima kerakligini va telefon raqamingizni yozing.":"Напишите, что вам нужно, и укажите номер телефона.",
    "So‘rov qabul qilindi":"Запрос принят",
    "Mos sotuvchilarga yuborildi":"Отправлено подходящим продавцам",
    "Yo‘nalishni aniqlashtiryapmiz":"Уточняем категорию",
    "Taklif kelishi bilan shu yerda ko‘rasiz.":"Предложение появится здесь, как только поступит.",
    "Taklif kelishi bilan shu yerda ko‘rasiz. Sahifani yopib qaytsangiz ham saqlanadi.":"Предложение появится здесь, как только поступит. Запрос сохранится, даже если вы закроете страницу.",
    "Noto‘g‘ri sotuvchilarga yubormaymiz; so‘rov aniqlangach tarqatiladi.":"Мы не отправляем запрос случайным продавцам; он уйдёт после уточнения.",
    "Noto‘g‘ri sotuvchilarga yubormaymiz; so‘rov aniqlangach tarqatiladi. Sahifani yopib qaytsangiz ham saqlanadi.":"Мы не отправляем запрос случайным продавцам; он уйдёт после уточнения. Запрос сохранится, даже если вы закроете страницу.",
    "Sahifani yopib qaytsangiz ham saqlanadi.":"Запрос сохранится, даже если вы закроете страницу.",
    "Hali javob yo‘q — kutyapmiz.":"Ответов пока нет — ожидаем.",
    "yangi javob":"новый ответ",
    "Bor":"В наличии",
    "O‘XSHASHI BOR":"ЕСТЬ АНАЛОГ",
    "Onlayn holati noma’lum":"Статус в сети неизвестен",
    "Xabarni ko‘rish":"Открыть сообщение",
    "Narxlar kelishiladi":"Цена договорная",
    "Bozordagi narx oralig‘i":"Диапазон цен на рынке",
    "Chetdagi noodatiy narxlar chiqarib tashlangan.":"Необычные крайние цены исключены.",
    "Odatiy narx":"Обычная цена",
    "Eng arzoni":"Самая низкая",
    "Arzon takliflar":"Недорогие предложения",
    " dan":" от",
    "Mos taklif":"Подходят",
    "Aniq qidiruv":"Точный поиск",
    "So‘rovni tushundik":"Мы поняли запрос",
    "Mos kelmaydigan mashina va qismlar natijadan kesildi.":"Неподходящие автомобили и детали исключены из результатов.",
    "Umumiy qidiruv":"Общий поиск",
    "Ehtiyot qism":"Запчасть",
    "KELISHILADI":"ДОГОВОРНАЯ",
    "DO‘KON":"МАГАЗИН",
    "YANGI":"НОВОЕ",
    "Hozircha tayyor e’lon yo‘q":"Готовых объявлений пока нет",
    "So‘rovni aniqlashtirish kerak":"Нужно уточнить запрос",
    "Yo‘nalishni tushundik. Endi mos sotuvchilardan bugungi aniq taklifni so‘raymiz.":"Категория понятна. Теперь запросим актуальное предложение у подходящих продавцов.",
    "Noto‘g‘ri mahsulot ko‘rsatmaymiz. So‘rov tekshirilib, faqat mos yo‘nalishga yuboriladi.":"Мы не показываем неподходящие товары. Запрос будет проверен и отправлен только нужной категории.",
    "Mos takliflar":"Подходящие предложения",
    "Yangi javoblar":"Новые ответы",
    "Javoblarni yopish":"Закрыть ответы",
    "so‘rovingiz":"ваш запрос",
    "Banner va tashqi reklama":"Баннеры и наружная реклама",
    "Ko‘rish":"Открыть",
    "Yashirish":"Скрыть",

    "Kerakli xaridor sizni o‘zi topadi.":"Нужный покупатель сам найдёт вас.",
    "Sizning mahsulot yoki xizmatingizga mos so‘rov kelganda, chatda javob yozing.":"Когда придёт подходящий запрос на ваш товар или услугу, ответьте в чате.",
    "Sizning mahsulot yoki xizmatingizga mos so‘rov kelganda, bir tegishda javob bering.":"Когда появится запрос на ваш товар или услугу, ответьте одним нажатием.",
    "Nima sotishingizni o‘z so‘zingiz bilan yozing.":"Опишите своими словами, что вы продаёте.",
    "Faqat sizga mos xaridor so‘rovlarini ko‘ring.":"Получайте только подходящие запросы покупателей.",
    "Chatda narx va xabarni 10 soniyada yuboring.":"Отправьте цену и сообщение в чате за 10 секунд.",
    "Bor-yo‘qligi va narxini 10 soniyada yuboring.":"Отправьте наличие и цену за 10 секунд.",
    "Kategoriya daraxti va uzoq anketa yo‘q.":"Без дерева категорий и длинной анкеты.",
    "Telefon raqamingiz va Telegram orqali kelgan kod bilan istalgan qurilmadan kirasiz. Yangi so‘rov va xaridor xabari Telegram’ga ham keladi.":"Входите с любого устройства по номеру телефона и коду из Telegram. Новые запросы и сообщения покупателей также приходят в Telegram.",
    "30 soniya · kategoriya tanlash yo‘q":"30 секунд · без выбора категории",
    "Sotuvchi sifatida boshlang":"Начать как продавец",
    "30 soniyada tayyor. Kategoriya daraxti va uzun anketa yo‘q. Odamlar qanday so‘rasa, shunday yozing.":"Готово за 30 секунд. Без дерева категорий и длинной анкеты. Пишите так, как спрашивают люди.",
    "Ro‘yxatdan tanlamang — odamlar qanday so‘rasa, shunday yozing.":"Не выбирайте из списка — пишите так, как спрашивают люди.",
    "Ismingiz yoki biznes nomi":"Ваше имя или название бизнеса",
    "Masalan: Aziz yoki Print House":"Например: Азиз или Print House",
    "Masalan: mebel yasayman yoki texnika tuzataman":"Например: делаю мебель или ремонтирую технику",
    "Nima sotasiz yoki qanday xizmat ko‘rsatasiz?":"Что вы продаёте или какие услуги оказываете?",
    "o‘z so‘zingiz bilan":"своими словами",
    "Banner chop etish, fara yoki stop":"Печать баннеров, фары или стоп-сигналы",
    "Qayerdasiz?":"Где вы находитесь?",
    "yaqin so‘rovlar uchun":"для ближайших запросов",
    "faqat kirish va xavfsizlik uchun, xaridorga ko‘rsatilmaydi":"только для входа и безопасности, покупателю не показывается",
    "akkaunt va OBER bildirishnomalari uchun":"для аккаунта и уведомлений OBER",
    "So‘rovlarni ko‘rish":"Смотреть запросы",
    "Mos so‘rovlarni ko‘rish":"Смотреть подходящие запросы",
    "Shu mahsulotni so‘rash":"Спросить об этом товаре",
    "So‘rov mos sotuvchilarga boradi. To‘lov va yetkazish OBER orqali bajarilmaydi.":"Запрос уйдёт подходящим продавцам. Оплата и доставка не проводятся через OBER.",
    "Nom, yo‘nalish, joy va telefon raqamini to‘ldiring.":"Укажите имя, направление, местоположение и номер телефона.",
    "Ro‘yxatdan o‘tib bo‘lmadi":"Не удалось зарегистрироваться",
    "Tushundik:":"Мы поняли:",
    "Aloqa xatosi. Qayta urinib ko‘ring.":"Ошибка соединения. Попробуйте ещё раз.",
    "So‘rovlar yuklanmoqda":"Запросы загружаются",
    "Hozircha yangi so‘rov yo‘q":"Новых запросов пока нет",
    "Akkaunt xavfsizligi":"Безопасность аккаунта",
    "Kirishni tiklashni yoqing":"Включите восстановление входа",
    "Kirishga bog‘lash":"Привязать для входа",
    "Telegram’ga ulansangiz, yangi so‘rov va xaridor xabari telefoningizga keladi.":"Подключите Telegram, чтобы новые запросы и сообщения покупателей приходили на телефон.",
    "Sizning yo‘nalishingizda xaridor so‘rov qoldirsa, shu yerda paydo bo‘ladi.":"Когда покупатель оставит запрос по вашему направлению, он появится здесь.",
    "Sahifa ochiq tursa, ro‘yxat o‘zi yangilanadi.":"Пока страница открыта, список обновляется автоматически.",
    "Jonli so‘rovlar":"Живые запросы",
    "Xaridorlar kutyapti":"Покупатели ждут",
    "Bir tegishda javob bering — taklif xaridorga OBER ichida boradi.":"Ответьте одним нажатием — предложение уйдёт покупателю внутри OBER.",
    "ochiq so‘rov":"открытых запросов",
    "So‘rovlarni hozir yuklay olmadik. Internetni tekshirib, sahifani yangilang.":"Не удалось загрузить запросы. Проверьте интернет и обновите страницу.",
    "YAQIN":"РЯДОМ",
    "BOR":"ЕСТЬ",
    "YO‘Q":"НЕТ",
    "Narxi":"Цена",
    "Narxi (so‘m)":"Цена (сум)",
    "Narx":"Цена",
    "Narx dan":"Цена от",
    "Narx gacha":"Цена до",
    "Byudjet:":"Бюджет:",
    "dan":"от",
    "gacha":"до",
    "Mosligi bo‘yicha":"По релевантности",
    "Avval arzoni":"Сначала дешевле",
    "Avval yangisi":"Сначала новые",
    "Avval yaqini":"Сначала ближе",
    "Chegarasiz ko‘rish":"Смотреть без границы",
    "Sotuvchilardan so‘rash":"Спросить продавцов",
    "Bugun kimda borligini sotuvchilarning o‘zidan so‘raymiz.":"Спросим у продавцов, у кого это есть сегодня.",
    "Keraklisi topilmadimi?":"Не нашли нужное?",
    "Indeksda yo‘q — jonli so‘raymiz.":"В индексе нет — спросим напрямую.",
    "Xaridorga xabar":"Сообщение покупателю",
    "Masalan: original, hozir bor":"Например: оригинал, есть в наличии",
    "Rasm qo‘shish":"Добавить фото",
    "Rasm tayyor":"Фото готово",
    "Chatga yuborish":"Отправить в чат",
    "Bu menda yo‘q":"У меня этого нет",
    "Xabar yozing… Masalan: original, hozir bor":"Напишите сообщение… Например: оригинал, есть в наличии",
    "Rasmni o‘qib bo‘lmadi":"Не удалось прочитать фото",
    "Javob yuborilmadi":"Ответ не отправлен",
    "Javob yuborildi":"Ответ отправлен",
    "Javob yuborildi — taklif va xabar xaridorga yetdi":"Ответ отправлен — предложение и сообщение доставлены покупателю",
    "Xabarlarni ochish":"Открыть сообщения",
    "Chatni ochish":"Открыть чат",

    "Bildirishnomalar":"Уведомления",
    "Takliflaringiz":"Ваши диалоги",
    "Jonli javoblar shu yerda ko‘rinadi.":"Здесь появится переписка с продавцом.",
    "Sotuvchi takliflari":"Диалоги с продавцами",
    "Yuklanmoqda…":"Загрузка…",
    "OBER ichki yozishmasi":"Внутренняя переписка OBER",
    "Orqaga":"Назад",
    "Taklif":"Предложение",
    "Yuboriladigan rasm":"Фото для отправки",
    "Rasm xabarga qo‘shiladi":"Фото будет добавлено к сообщению",
    "Olib tashlash":"Удалить",
    "Rasm":"Фото",
    "Kamera yoki galereyadan rasm tanlash":"Выбрать фото из камеры или галереи",
    "Xabar yozing…":"Напишите сообщение…",
    "Kamera yoki galereya · JPG, PNG, WEBP · 5 MB gacha":"Камера или галерея · JPG, PNG, WEBP · до 5 МБ",
    "Barchasini o‘qish":"Отметить всё прочитанным",
    "Yopish":"Закрыть",
    "Brauzer xabarlari":"Уведомления браузера",
    "OBER ochiq turganda yangi javobni darhol biling.":"Узнавайте о новом ответе сразу, пока OBER открыт.",
    "Yoqish":"Включить",
    "Mavjud emas":"Недоступно",
    "Bu brauzer bildirishnomalarni qo‘llamaydi.":"Этот браузер не поддерживает уведомления.",
    "Yoqilgan":"Включено",
    "Yangi javob kelganda OBER sizga darhol bildiradi.":"OBER сразу сообщит о новом ответе.",
    "Bloklangan":"Заблокировано",
    "Brauzer sozlamasidan OBER xabarlariga ruxsat bering.":"Разрешите уведомления OBER в настройках браузера.",
    "Brauzer sozlamasidan ruxsat bering":"Разрешите уведомления в настройках браузера",
    "Brauzer xabarlari yoqildi":"Уведомления браузера включены",
    "OBER’da yangi xabar":"Новое сообщение в OBER",
    "Yangi xabar keldi":"Поступило новое сообщение",
    "Hammasi joyida":"Всё в порядке",
    "Jonli takliflar":"Живые предложения",
    "Yangi taklif yoki xabar hozircha yo‘q.":"Новых сообщений пока нет.",
    "Hammasi o‘qildi":"Всё отмечено прочитанным",
    "Qayta urinib ko‘ring":"Попробуйте ещё раз",
    "Hali faol so‘rov yo‘q":"Активных запросов пока нет",
    "Bosh sahifadan jonli so‘rov yuboring.":"Отправьте живой запрос с главной страницы.",
    "Bosh sahifaga qaytish":"Вернуться на главную",
    "Kabinetingiz bitta raqamga bog‘langan.":"Ваш кабинет привязан к одному номеру.",
    "Telefon raqamingiz va Telegram orqali kelgan kod bilan istalgan qurilmadan kirasiz — xabarlar va kabinet saqlanadi.":"Входите с любого устройства по номеру телефона и коду из Telegram — сообщения и кабинет сохраняются.",
    "Telefon raqamingizni kiriting.":"Введите номер телефона.",
    "Kod Telegram’ga keladi.":"Код придёт в Telegram.",
    "Kodni kiriting — kabinet ochiladi.":"Введите код — кабинет откроется.",
    "Ro‘yxatdan o‘tganmisiz? Shu raqam orqali kiring.":"Уже зарегистрированы? Войдите по этому номеру.",
    "Kabinetga kirish":"Вход в кабинет",
    "Telefon raqamingizni yozing. Bir martalik kod Telegram’ga yuboriladi.":"Укажите номер телефона. Разовый код придёт в Telegram.",
    "Kod olish":"Получить код",
    "Telegram’ga kelgan kod":"Код из Telegram",
    "6 raqam":"6 цифр",
    "Kirish":"Войти",
    "Yangi sotuvchimisiz?":"Новый продавец?",
    "Ro‘yxatdan o‘tish":"Зарегистрироваться",
    "Telefon raqamini to‘ldiring.":"Укажите номер телефона.",
    "Kod Telegram’ga yuborildi. Telegram’ni oching.":"Код отправлен в Telegram. Откройте Telegram.",
    "bu raqam ro'yxatdan o'tmagan":"этот номер не зарегистрирован",
    "kirish uchun avval Telegramga ulanish kerak. Birinchi qurilmadagi kabinetda “Telegramga ulash”ni bosing.":"для входа сначала нужно подключить Telegram. Нажмите «Подключить Telegram» в кабинете на первом устройстве.",
    "Kod noto‘g‘ri":"Неверный код",
    "Kirdingiz. Kabinet ochilmoqda…":"Вы вошли. Открываем кабинет…",
    "Allaqachon ro‘yxatdan o‘tganmisiz?":"Уже зарегистрированы?",
    "Telefon raqami va kodni to‘ldiring.":"Укажите номер телефона и код.",
    "kod noto'g'ri yoki eskirgan":"код неверный или истёк",
    "Xaridorlar bilan suhbatlar":"Диалоги с покупателями",
    "Taklif va yangi xabarlar bir joyda.":"Предложения и новые сообщения — в одном месте.",
    "Xaridor":"Покупатель",
    "Ulanib bo‘lmadi":"Не удалось подключиться",
    "Sahifani yangilab ko‘ring.":"Обновите страницу и попробуйте снова.",
    "Chatga ulanib bo‘lmadi":"Не удалось подключиться к чату",
    "Internetni tekshirib, suhbatlarni yana yuklab ko‘ring.":"Проверьте интернет и загрузите диалоги ещё раз.",
    "Hali taklif kelmadi":"Диалогов пока нет",
    "Mos sotuvchilar javob berishi bilan shu yerda ko‘rinadi.":"Диалог появится здесь, когда ответит продавец.",
    "TASDIQLANGAN":"ПРОВЕРЕН",
    "Taklif yuborildi":"Сообщение отправлено",
    "Xabardagi rasm":"Фото в сообщении",
    "Taklif tanlanmadi":"Не удалось выбрать предложение",
    "Narx kelishiladi":"Цена договорная",
    "Hozir bor":"В наличии",
    "Ertaga":"Завтра",
    "Suhbatda yuborilgan rasm":"Фото в переписке",
    "Siz":"Вы",
    "Bu chat aloqa uchun. To‘lov va yetkazish OBER orqali bajarilmaydi.":"Этот чат предназначен для связи. Оплата и доставка не проводятся через OBER.",
    "Sotuvchi bilan aniqlashtiring. To‘lov va yetkazish OBERda bajarilmaydi.":"Уточните детали у продавца. Оплата и доставка не проводятся в OBER.",
    "Kerakli narsani topdingizmi? Javob OBERni yaxshilashga yordam beradi.":"Вы нашли нужное? Ответ поможет улучшить OBER.",
    "Ha, OBER orqali":"Да, через OBER",
    "Ha, boshqa joydan":"Да, в другом месте",
    "Hali topmadim":"Пока не нашёл",
    "JPG, PNG yoki WEBP · 5 MB gacha":"JPG, PNG или WEBP · до 5 МБ",
    "5 MB gacha":"до 5 МБ",
    "Xabar yuborilmadi":"Сообщение не отправлено",
    "Xaridordan yangi xabar":"Новое сообщение от покупателя",
    "Qidiruvga qaytish":"Вернуться к поиску",
    "← Qidiruvga qaytish":"← Вернуться к поиску",
    "Rasm yo‘q":"Нет фото",
    "SOTUVCHI":"ПРОДАВЕЦ",
    "OBER orqali aloqaga chiqing. Telefon raqamini sotuvchi o‘zi bergan.":"Свяжитесь через OBER. Номер телефона указал сам продавец.",
    "Telefon raqamini ko‘rsatish":"Показать номер телефона",
    "E‘lon topilmadi":"Объявление не найдено",
    "Bu e‘lon mavjud emas yoki o‘chirilgan bo‘lishi mumkin.":"Этого объявления нет или оно было удалено.",
    "Bugun":"Сегодня",
    "Kecha":"Вчера",
    "So‘rovlar":"Запросы",
    "E‘lonlarim":"Мои объявления",
    "Tavsiya etiladi":"Рекомендуется",
    "Telegramga ulash":"Подключить Telegram",
    "So‘rovni o‘tkazib yubormang":"Не пропустите запрос",
    "Taklifni yuboring, keyin chatda aniqlashtiring. Savdo OBERdan tashqarida yakunlanadi.":"Отправьте предложение и уточните детали в чате. Сделка завершается вне OBER.",
    "Telegramga ulasangiz, sahifani ochib o'tirish shart emas.":"Если подключите Telegram, не нужно сидеть с открытой страницей.",
    "Suhbatlar":"Диалоги",
    "Sotuvchi bilan yozishmalar shu yerda.":"Переписка с продавцом будет здесь.",
    "Vaqtim ko‘rinsin":"Показывать моё время",
    "Vaqtim yashirin":"Моё время скрыто",
    "Joylashuv":"Геолокация",
    "Hali suhbat yo‘q":"Диалогов пока нет",
    "ochiq e’lon · OLX va Telegram · har 45 daqiqada yangilanadi":"открытых объявлений · OLX и Telegram · обновляется каждые 45 минут",

    // ── Kategoriya namunalari (OLX kichik bo'limlari) ──────────────────
    "Mebel":"Мебель",
    "Avtobuslar":"Автобусы",
    "Avtomashina uchun aksessuarlar":"Автоаксессуары",
    "Avto ehtiyot qismlar":"Автозапчасти",
    "Avtotovush":"Автозвук",
    "avtoregistratorlar":"видеорегистраторы",
    "Ehtiyot qismlarga ajratilgan transport":"Транспорт на запчасти",
    "Boshqa transport":"Другой транспорт",
    "Yuk mashinalari":"Грузовики",
    "Ijara uzoq muddatga":"Долгосрочная аренда",
    "Sotish":"Продажа",
    "Ijara":"Аренда",
    "Dacha":"Дача",
    "Hostel":"Хостел",
    "Kvartiralar":"Квартиры",
    "Otellar":"Отели",
    "Dam olish maskanlari":"Места отдыха",
    "Aksessuarlar va komplekt jihozlar":"Аксессуары и комплекты",
    "Akustika tizimlari":"Акустические системы",
    "vinil ovoz chiqargichlar":"виниловые проигрыватели",
    "Magnitolalar":"Магнитолы",
    "Mp3 pleterlari":"MP3-плееры",
    "Musiqa markazlari":"Музыкальные центры",
    "Naushniklar":"Наушники",
    "Portativ akustika":"Портативная акустика",
    "Boshqa audiotexnika":"Другая аудиотехника",
    "Radiopriyomniklar":"Радиоприёмники",
    "Ovoz kuchaytirgichlar-resiverlar":"Усилители и ресиверы",
    "videokameralar uchun aksessuarlar":"аксессуары для видеокамер",
    "Havo yangilash va dezinfeksiya":"Очистка и дезинфекция воздуха",
    "Tozalash uchun":"Для уборки",
    "Konteyner va idishlar":"Контейнеры и ёмкости",
    "Basseynlar uchun":"Для бассейнов",
    "Kir yuvish va quritish uchun":"Для стирки и сушки",
    "Benzoinstrument":"Бензоинструмент",
    "Bulg'orlar":"Болгарки",
    "Qurilish mikserlari":"Строительные миксеры",
    "Qurilish changyutgichlari":"Строительные пылесосы",
    "Drellar va shurupburagichlar":"Дрели и шуруповёрты",
    "Qurilish fenlari":"Строительные фены",
    "Karavot panellari":"Панели кроватей",
    "Bolalar shkaflari":"Детские шкафы",
    "Bolalar mebel to'plamlari":"Детские мебельные комплекты",
    "Bolalar karavotlari va beshiklar":"Детские кровати и колыбели",
    "Bolalar komodlari":"Детские комоды",
    "Bolalar garniturlari":"Детские гарнитуры",
    "Bolalar shezlonglari":"Детские шезлонги",
    "Bolalar manejlari":"Детские манежи",
    "Bolalar matraslari":"Детские матрасы",
    "Bolalar stullari va stollari":"Детские стулья и столы",
    "Bolalar kreslolari":"Детские кресла",
    "Bijuteriya":"Бижутерия",
    "Boshqa aksessuarlar":"Другие аксессуары",
    "Sumkalar":"Сумки",
    "Zargarlik buyumlari":"Ювелирные изделия",
    "To'y aksessuarlari":"Свадебные аксессуары",
    "To'y liboslari":"Свадебные платья",
    "Biologik faol qo'shimchalar":"Биологически активные добавки",
    "Pardoz anjomlari":"Косметика",
    "Parfyumeriya":"Парфюмерия",
    "Go'zallik va salomatlik uchun boshqa mahsulotlar":"Другие товары для красоты и здоровья",
    "Parvarish vositalari":"Средства ухода",
    "Nogironlar uchun mahsulotlar":"Товары для людей с инвалидностью",
    "Avto elektrik xizmatlari":"Автоэлектрика",
    "ximchistka":"химчистка",
    "moto xizmatlari":"мотоуслуги",
    "bo'yash ishlari":"малярные работы",
    "Avtotamirlash":"Авторемонт",
    "skuterlarni ta'mirlash":"ремонт скутеров",
    "Boshqa maishiy xizmatlar":"Другие бытовые услуги",
    "qulfni ochish":"вскрытие замков",
    "Universal usta":"Универсальный мастер",
    "poyabzal ta'mirlash":"ремонт обуви",
    "Soat ta'mirlash":"Ремонт часов",
    "mebelni tiklash":"реставрация мебели",
    "Avtoservis":"Автосервис",
    "menejer":"менеджер",
    "barista":"бариста",
    "Kassir":"Кассир",
    "Ofitsiant":"Официант",
    "qandolatchi":"кондитер",
    "oshpaz":"повар",
    "fast food":"фастфуд",
    "idish yuvuvchi":"посудомойщик",
    "Ofis":"Офис",
    "Qisman bandlik":"Частичная занятость",
    "Akvarium baliqlari":"Аквариумные рыбки",
    "Topilmalar idorasi":"Бюро находок",
    "Boshqa hayvonlar":"Другие животные",
    "Kemiruvchilar":"Грызуны",
    "Mushuklar":"Кошки",
    "Qushlar":"Птицы",
    "Qishloq xo'jalik hayvonlari":"Сельскохозяйственные животные",
    "Itlar":"Собаки",
    "Hayvonlar uchun sumkalar":"Сумки для животных",
    "Hayvonlar uchun kiyim-kechak":"Одежда для животных",
    "Hayvonlar uchun oziq-ovqat":"Корм для животных",
    "Hayvonlar uchun uycha":"Домики для животных",
    "Antikvar mebellar":"Антикварная мебель",
    "Bukinistika":"Букинистика",
    "Kolleksiyalash":"Коллекционирование",
    "Qo'lda tayyorlangan mahsulotlar":"Изделия ручной работы",
    "San'at buyumlari":"Предметы искусства",
    "Rassomlik":"Живопись",
    "Chiptalar":"Билеты",
    "Cd-dvd-plastinkalar, kassetalar":"CD/DVD-диски, кассеты",
    "Boshqalar":"Другое",
    "Kitoblar-jurnallar":"Книги и журналы",
    "Musiqa asboblari uchun aksessuarlar":"Аксессуары для музыкальных инструментов",
    "Puflab chalinadigan musiqa asboblari":"Духовые музыкальные инструменты",
    "Boshqa":"Другое"
  };

  // Tutuq belgisi har xil ko'rinishda bo'lishi mumkin: ASCII ' (U+0027),
  // ‘ (U+2018) yoki ’ (U+2019). Lug'at ham, sahifadagi matn ham har xil
  // ko'rinishda bo'lishi mumkin — ikkalasini ham normalizatsiya qilamiz.
  const RU_NORM = {};
  Object.keys(RU).forEach(k => {
    RU_NORM[k.replace(/[\u2018\u2019]/g, "'")] = RU[k];
  });

  function translate(text) {
    if (lang !== "ru" || !text) return text;
    if (RU[text]) return RU[text];
    const compactText = text.replace(/\s+/g, " ").trim();
    if (compactText !== text && RU[compactText]) return RU[compactText];
    const normText = text.replace(/[\u2018\u2019]/g, "'");
    if (normText !== text && RU[normText]) return RU[normText];
    if (RU_NORM[normText]) return RU_NORM[normText];
    let match;
    if ((match = text.match(/^(\d+) ta suhbat$/))) return `${match[1]} чатов`;
    if ((match = text.match(/^(\d+) ta ochiq e’lon narxi va jonli sotuvchi javoblari$/))) return `${match[1]} цен открытых объявлений и живых ответов продавцов`;
    if ((match = text.match(/^(\d+) sotuvchi (?:chatda )?javob berdi$/))) return `Ответили продавцы: ${match[1]}`;
    if ((match = text.match(/^(.+) · (\d+) sotuvchi (?:chatda )?javob berdi$/))) return `${match[1]} · Ответили продавцы: ${match[2]}`;
    if ((match = text.match(/^(\d+) ta sotuvchi (?:chatda )?javob berdi$/))) return `Ответили продавцы: ${match[1]}`;
    if ((match = text.match(/^(\d+) ta natijadan eng moslari$/))) return `Лучшие из ${match[1]} результатов`;
    // Ruscha ko'plik: son uchun [1 → bir, 2-4 → ko'p, 5+ → juda ko'p]
    // shakllarini beradi. `kunlar` va `takliflar` ikkalasi ham shu orqali.
    const rusPlural = (n, [bir, kop, kopkop]) => {
      const m = n % 100;
      if (m >= 11 && m <= 14) return kopkop;
      const o = n % 10;
      return o === 1 ? bir : o >= 2 && o <= 4 ? kop : kopkop;
    };
    if ((match = text.match(/^(\d+\+?) ta taklif · (.+) dan$/))) {
      const son = parseInt(match[1], 10);
      return `${match[1]} ${rusPlural(son, ["предложение", "предложения", "предложений"])} · от ${match[2].replace(/ so[‘’']m$/, " сум")}`;
    }
    if ((match = text.match(/^(\d+\+?) ta taklif$/))) return `${match[1]} ${rusPlural(parseInt(match[1], 10), ["предложение", "предложения", "предложений"])}`;
    if ((match = text.match(/^(\d+\+?) ta e[’']lon · (.+) dan$/))) {
      const son = parseInt(match[1], 10);
      return `${match[1]} ${rusPlural(son, ["объявление", "объявления", "объявлений"])} · от ${match[2].replace(/ so[‘’']m$/, " сум")}`;
    }
    if ((match = text.match(/^(\d+\+?) ta e[’']lon$/))) return `${match[1]} ${rusPlural(parseInt(match[1], 10), ["объявление", "объявления", "объявлений"])}`;
    if ((match = text.match(/^Kategoriya: (.+)$/))) return `Категория: ${translate(match[1])}`;
    if ((match = text.match(/^(\d+) ta bo'lim$/))) return `${match[1]} ${rusPlural(+match[1], ['раздел', 'раздела', 'разделов'])}`;
    // Topildi qatorida raqam strong ichida, "· N so'm dan" esa alohida
    // text-node — uni alohida qoida bilan tarjima qilamiz.
    if ((match = text.match(/^· (.+) dan$/))) return `· от ${match[1].replace(/ so[‘’']m$/, " сум")}`;
    if ((match = text.match(/^(\d+) ta boshqa mashina chiqarildi$/))) return `Исключено других автомобилей: ${match[1]}`;
    if ((match = text.match(/^(\d+) ta yangi bildirishnoma$/))) return `Новых уведомлений: ${match[1]}`;
    if ((match = text.match(/^“(.+)” — (\d+) ta sotuvchi javob berdi$/))) return `“${match[1]}” — ответили продавцы: ${match[2]}`;
    if ((match = text.match(/^(\d+) daqiqada$/))) return `Через ${match[1]} минут`;
    // Sotuvchiga bildirishnoma: "Xaridor · Azizdan yangi xabar" (2026-08-08).
    if ((match = text.match(/^Xaridor · (.+)dan yangi xabar$/))) {
      return `Новое сообщение от покупателя · ${match[1]}`;
    }
    // Chatda xabar muallifi: Sotuvchi / Xaridor / Siz. Bitta qoida —
    // prefixlar bir-birini inkor etadi, uchta alohida qoidadan xavfsizroq.
    if ((match = text.match(/^(Sotuvchi|Xaridor|Siz) · (.+)$/))) {
      return `${{"Sotuvchi":"Продавец","Xaridor":"Покупатель","Siz":"Вы"}[match[1]]} · ${match[2]}`;
    }
    const OY_RU = {"yanvar":"января","fevral":"февраля","mart":"марта","aprel":"апреля","may":"мая","iyun":"июня","iyul":"июля","avgust":"августа","sentabr":"сентября","oktabr":"октября","noyabr":"ноября","dekabr":"декабря"};
    if ((match = text.match(/^(\d+) (yanvar|fevral|mart|aprel|may|iyun|iyul|avgust|sentabr|oktabr|noyabr|dekabr)$/))) {
      return `${match[1]} ${OY_RU[match[2]]}`;
    }
    // Ruscha kun-ko'plik: 1 kun, 2-4 kun, 5-20 kun, 21 kun, 22-24 kun, 25-30 kun...
    if ((match = text.match(/^(\d+) kun oldin$/))) return `${match[1]} ${rusPlural(+match[1], ["день", "дня", "дней"])} назад`;
    if ((match = text.match(/^(.+) · (\d+) (yanvar|fevral|mart|aprel|may|iyun|iyul|avgust|sentabr|oktabr|noyabr|dekabr)$/))) {
      return `${match[1]} · ${match[2]} ${OY_RU[match[3]]}`;
    }
    if ((match = text.match(/^(.+) · (\d+) kun oldin$/))) return `${match[1]} · ${match[2]} ${rusPlural(+match[2], ["день", "дня", "дней"])} назад`;
    if ((match = text.match(/^(.+) · (Bugun|Kecha)$/))) return `${match[1]} · ${match[2] === "Bugun" ? "Сегодня" : "Вчера"}`;
    // Emoji + matn (elon sahifasidagi meta: "🕐 Bugun", "📍 Chilonzor")
    if ((match = text.match(/^(🕐|📍|🏷) (.+)$/))) {
      const orta = translate(match[2]);
      return orta !== match[2] ? `${match[1]} ${orta}` : text;
    }
    if ((match = text.match(/^([\d\s]+) ta$/))) return match[1];
    if ((match = text.match(/^BYUDJET (.+)$/))) return `БЮДЖЕТ ${match[1].replace(/ so[‘’']m$/, " сум")}`;
    if ((match = text.match(/^Mashina: (.+)$/))) return `Автомобиль: ${match[1]}`;
    if ((match = text.match(/^Qism: (.+)$/))) return `Деталь: ${match[1]}`;
    if ((match = text.match(/^Yo‘nalish: (.+)$/))) return `Категория: ${translate(match[1])}`;
    if ((match = text.match(/^O‘qilmadi: (.+)$/))) return `Не отмечено: ${match[1]}`;
    if ((match = text.match(/^Telegramga ulasangiz, har so'rov telefoningizga keladi va\s+javobni ham o'sha yerda berasiz — bu sahifani ochish shart emas\.$/))) return `Если подключите Telegram, каждый запрос придёт на телефон и ответ дадите там же — открывать сайт не нужно.`;
    return text
      .replace(/ so[‘’']m/g, " сум")
      .replace(/ mln\b/g, " млн")
      .replace(/ ming\b/g, " тыс.")
      .replace(/ · Hozir bor/g, " · В наличии")
      .replace(/ · Ertaga/g, " · Завтра");
  }

  function translateTextNode(node) {
    const raw = node.nodeValue || "";
    const clean = raw.trim();
    if (!clean) return;
    const value = translate(clean);
    if (value !== clean) node.nodeValue = raw.replace(clean, value);
  }

  function translateElement(element) {
    if (!(element instanceof Element) || element.closest(".ober-lang-switch")) return;
    ["placeholder", "aria-label", "title", "alt"].forEach(name => {
      if (element.hasAttribute(name)) {
        const current = element.getAttribute(name);
        const value = translate(current);
        if (value !== current) element.setAttribute(name, value);
      }
    });
    // HTML o'qilishi uchun uzun gaplar bir necha qatorga bo'lingan bo'lishi
    // mumkin. Leaf elementda ularni bitta gap sifatida tarjima qilamiz.
    if (!element.children.length) {
      const raw = element.textContent || "";
      const clean = raw.replace(/\s+/g, " ").trim();
      const value = translate(clean);
      if (value !== clean) {
        element.textContent = value;
        return;
      }
    }
    element.childNodes.forEach(child => {
      if (child.nodeType === Node.TEXT_NODE) translateTextNode(child);
      else if (child.nodeType === Node.ELEMENT_NODE) translateElement(child);
    });
  }

  function addSwitcher() {
    const slot = document.querySelector(".lang-slot");
    if (!slot || slot.children.length) return;
    const style = document.createElement("style");
    style.textContent = `.ober-lang-switch{display:inline-flex;align-items:center;padding:3px;border:1px solid rgba(8,40,95,.13);border-radius:999px;background:rgba(255,255,255,.86);box-shadow:0 6px 18px rgba(8,40,95,.06)}.ober-lang-switch button{min-width:34px;height:28px;padding:0 8px;border:0;border-radius:999px;background:transparent;color:#69758a;font:800 11px/1 Inter,ui-sans-serif,system-ui,sans-serif;cursor:pointer}.ober-lang-switch button.active{background:#08285f;color:#fff}.ober-lang-switch button:focus-visible{outline:3px solid rgba(36,113,220,.28);outline-offset:2px}@media(max-width:520px){.ober-lang-switch button{min-width:31px;padding:0 6px}.ober-lang-switch{padding:2px}}`;
    document.head.appendChild(style);
    slot.innerHTML = `<div class="ober-lang-switch" role="group" aria-label="Til / Язык"><button type="button" data-lang="uz" class="${lang === "uz" ? "active" : ""}">O‘z</button><button type="button" data-lang="ru" class="${lang === "ru" ? "active" : ""}">Рус</button></div>`;
    slot.querySelectorAll("button").forEach(button => button.addEventListener("click", () => {
      const next = button.dataset.lang;
      if (next !== lang) { localStorage.setItem(STORAGE_KEY, next); location.reload(); }
    }));
  }

  function init() {
    document.documentElement.lang = lang;
    if (lang === "ru") {
      document.title = translate(document.title);
      translateElement(document.body);
      new MutationObserver(records => records.forEach(record => {
        record.addedNodes.forEach(node => {
          if (node.nodeType === Node.TEXT_NODE) translateTextNode(node);
          else if (node.nodeType === Node.ELEMENT_NODE) translateElement(node);
        });
      })).observe(document.body, {childList:true, subtree:true});
    }
    addSwitcher();
  }

  window.OBER_I18N = {lang, locale:lang === "ru" ? "ru-RU" : "uz-UZ", t:translate, init};
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, {once:true});
  else init();
})();
