# Python Tekstdan Quiz Yaratuvchi 

Python Quiz Generator paketi, sizga formatlangan matn kiruvchidan testlarni yaratishga imkon beradi. U kiritilgan matnni tahlil qiladi va savollar va variantlar bilan test obyektlarini yaratadi.

## O'rnatish

Python Quiz Generatorni pip yordamida o'rnatishingiz mumkin:

```bash
pip install ttq
```

## Foydalanish

### Kiruvchi Matn Formati

Kiruvchi matn ma'lum bir formatni qo'llab-quvvatlashi kerak:

- Har bir savol so'rovnoma matnidan boshlanishi va `{` bilan variantlar qismi davom etishi kerak.
- Har bir variant `=`, `~` belgilar bilan boshlanishi kerak, `=` variantning to'g'riligini ko'rsatadi.
- Har bir savol variantlari `}` bilan tugashi kerak.

Masalan:

```
Savol matni {
= To'g'ri variant 1
~ Noto'g'ri variant 1
~ Noto'g'ri variant 2
}

Savol matni {
= To'g'ri variant 1
~ Noto'g'ri variant 1
}

Savol matni {
= To'g'ri variant 1
~ Noto'g'ri variant 1
= To'g'ri variant 2
}

...

```

### Kiruvchi Matnni Tahlil Qilish

Kiruvchi matnni tahlil qilish uchun `parse_text` funktsiyasidan foydalanishingiz mumkin va `Quiz` obyektini yaratishingiz mumkin:

```python
from ttq import parse_text

input_text = """
To'g'ri Savol 1{
= To'g'ri variant 1
~ Noto'g'ri variant 1
~ Noto'g'ri variant 2
}

To'g'ri Savol 2{
= To'g'ri variant 1
~ Noto'g'ri variant 1
= To'g'ri variant 2
}

Noto'g'ri Savol 1{
~ Noto'g'ri variant 1
~ Noto'g'ri variant 2
}

Noto'g'ri Savol 2{
= To'g'ri variant 1
= To'g'ri variant 2
}
"""

quiz = parse_text(input_text)
```

Bu yerda ikkita noto'g'ri savollar mavjud. Birinchisida to'g'ri variantlar berilmagan, ikkinchisida noto'g'risi.

### Quiz Obyektiga Murojat Qilish

Bir marta `Quiz` obyektini olgandan so'ng, savollariga va variantlariga murojat qila olasiz:

```python
for savol in quiz.questions:
    print(savol.text, savol.type)
    for variant in savol.options:
        print(variant.text)
```

## Ishga tushirish

Ishonch bildiramiz! Agar sizda tashrif buyurgan savollar yoki takliflar bo'lsa, iltimos, GitHubda savol oching yoki pull so'rov yaratib qo'ying.

## Ruxsatnoma

Ushbu loyiha MIT litsenziyasi asosida litsenziyalangan - to'liq ma'lumotlar uchun [LITSENZIYA](LICENSE) faylini ko'ring.
