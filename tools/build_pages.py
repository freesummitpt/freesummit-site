"""Generates the activity pages (guia/, via-ferrata/, ...) from one template.
Edit the PAGES data below, then run from anywhere:  python3 tools/build_pages.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root = the website

def t(en, pt):
    """Bilingual text node helper: returns attrs+text for an element."""
    return f'data-pt="{pt}">{en}'

FORM_OPTIONS = [
    ("Rock climbing at Guia (Cascais)", "Escalada na Guia (Cascais)"),
    ("Via Ferrata dos Pinheirinhos (Sesimbra)", None),
    ("Arrábida hiking tour", "Caminhada na Serra da Arrábida"),
    ("Rock climbing at Fenda da Arrábida", "Escalada na Fenda da Arrábida"),
    ("Rock climbing at Forte do Cavalo (Sesimbra)", "Escalada no Forte do Cavalo (Sesimbra)"),
    ("Full day in Sesimbra (combo)", "Dia inteiro em Sesimbra (combo)"),
    ("Not sure yet", "Ainda não sei"),
]

PAGES = {
 "guia": dict(
   slug="guia", form_value="Rock climbing at Guia (Cascais)",
   title_en="Rock climbing in Cascais · Free Summit",
   meta_en="Guided outdoor rock climbing at Guia, Cascais. No experience needed. Guide, climbing shoes, all gear and insurance included. From €45 per person.",
   place="Cascais", coords="38.70° N, 9.45° W",
   h1=("Rock climbing in Cascais", "Escalada em Cascais"),
   sub=("Your first time on real rock, on a sea cliff by the Guia lighthouse. No experience needed: we bring the gear, set the ropes and teach you everything.",
        "A tua primeira vez na rocha, numa falésia junto ao farol da Guia. Não precisas de experiência: levamos o material, montamos as cordas e ensinamos-te tudo."),
   price="€45",
   facts=[(("Duration","Duração"),("~4 hours","~4 horas")),(("Level","Nível"),("Beginner","Iniciação")),(("Min. age","Idade mín."),("10 years","10 anos")),(("Group","Grupo"),("2 to 6","2 a 6")),(("Approach","Aproximação"),("Under 5 min","Menos de 5 min"))],
   about=[("A half-day introduction to outdoor climbing on the limestone cliffs next to the Guia lighthouse, with the Atlantic right in front of you.",
           "Um meio-dia de iniciação à escalada nas falésias de calcário junto ao farol da Guia, com o Atlântico mesmo à tua frente."),
          ("The crag is a few minutes from the road and has around 100 well-bolted routes. You climb on top-rope, with the guide setting every anchor and checking every belay. Beginners start on the easier slabs; if you already climb, you can move on to harder lines.",
           "A falésia fica a poucos minutos da estrada e tem cerca de 100 vias bem equipadas. Escalas em top-rope, com o guia a montar todas as ancoragens e a verificar cada segurança. Quem começa faz as placas mais fáceis; quem já escala pode passar a vias mais difíceis."),
          ("It works well for families, couples and travellers staying in Cascais or Lisbon. Come by train on the Cascais line and we pick you up at the station for free.",
           "É ideal para famílias, casais e para quem está em Cascais ou Lisboa. Vem de comboio pela linha de Cascais e vamos buscar-te à estação sem custos.")],
   included=[("Guide with you the whole time","Guia sempre contigo"),("Harness, helmet and climbing shoes in all sizes","Arnês, capacete e sapatilhas de escalada em todos os tamanhos"),("Ropes, belay devices and chalk","Cordas, aparelhos de segurança e magnésio"),("Activity insurance","Seguro de actividade"),("Photos of your climbs","Fotografias da actividade"),("Free pick-up at Cascais train station","Recolha grátis na estação de Cascais")],
   plan=[(("Meet","Encontro"),("Welcome, gear fitting and safety briefing by the lighthouse.","Boas-vindas, ajuste do material e briefing junto ao farol.")),
         (("Down to the crag","Descida à falésia"),("A short walk and a flight of stairs to the rock.","Uma pequena caminhada e umas escadas até à rocha.")),
         (("Skills","Técnica"),("Knots, belaying and climbing calls. The guide checks every belay.","Nós, segurar e comandos de escalada. O guia verifica cada segurança.")),
         (("Climb","Escalar"),("Routes of rising difficulty, taking turns climbing and belaying.","Vias de dificuldade crescente, à vez a escalar e a segurar.")),
         (("Finish","Fim"),("Pack up and debrief. We send you the photos afterwards.","Arrumar e conversa final. Enviamos as fotos depois."))],
   prices=[(("Shared group","Grupo partilhado"),"€45"),(("Private, 2 people (each)","Privado, 2 pessoas (cada)"),"€45"),(("Private, each extra person","Privado, cada pessoa a mais"),"€35"),(("Children 10–15","Crianças 10–15"),"€35"),(("Full day, ~6 h (shared)","Dia inteiro, ~6 h (partilhado)"),"€75"),(("Solo private (total)","Privado, 1 pessoa (total)"),"€110"),(("Transfer from Lisbon, round trip","Transfer desde Lisboa, ida e volta"),"+€20"),(("Pick-up at Cascais station","Recolha na estação de Cascais"),("Free","Grátis"))],
   note=("Minimum 2 participants per departure. In summer we climb in the morning or late afternoon, as the cliff gets sun all day.",
         "Mínimo de 2 participantes por saída. No verão escalamos de manhã ou ao fim da tarde, porque a falésia apanha sol todo o dia."),
   bring=[(("Shoes:","Calçado:"),("trainers for the walk in (climbing shoes are provided).","ténis para a caminhada (as sapatilhas de escalada são nossas).")),(("Clothes:","Roupa:"),("comfortable sports clothing that lets you move freely.","desportiva e confortável, que te deixe mexer à vontade.")),(("Water:","Água:"),("1 to 1.5 L and a snack.","1 a 1,5 L e um snack.")),(("Sun:","Sol:"),("sunscreen, sunglasses and a cap.","protector solar, óculos de sol e boné."))],
 ),
 "via-ferrata": dict(
   slug="via-ferrata", form_value="Via Ferrata dos Pinheirinhos (Sesimbra)",
   title_en="Via ferrata in Sesimbra · Free Summit",
   meta_en="Guided via ferrata at Pinheirinhos, Sesimbra: 800 m along the sea cliffs of Arrábida. No climbing experience needed. Guide, gear and insurance included. €65 per person.",
   place="Sesimbra", coords="38.43° N, 9.13° W",
   h1=("Via ferrata over the Atlantic", "Via ferrata sobre o Atlântico"),
   sub=("800 metres along the sea cliffs of Pinheirinhos, Sesimbra, clipped to a steel cable the whole way. No climbing experience needed, just a head for heights.",
        "800 metros pelas falésias dos Pinheirinhos, em Sesimbra, sempre preso a um cabo de aço. Não precisas de experiência em escalada, só de gostar de alturas."),
   price="€65",
   facts=[(("Duration","Duração"),("~4 hours","~4 horas")),(("Route","Percurso"),("800 m · K3","800 m · K3")),(("Height gain","Desnível"),("195 m","195 m")),(("Min. age","Idade mín."),("12 years","12 anos")),(("Group","Grupo"),("2 to 8","2 a 8"))],
   about=[("A half-day via ferrata along the limestone cliffs west of Sesimbra, inside the Arrábida Natural Park, with the Luiz Saldanha Marine Park below you the whole way.",
           "Uma via ferrata de meio-dia pelas falésias de calcário a oeste de Sesimbra, dentro do Parque Natural da Arrábida, com o Parque Marinho Luiz Saldanha sempre por baixo."),
          ("The route traverses the cliffs on steel cables, rungs and some fixed ropes. You are clipped in at all times with an energy-absorbing lanyard, and your guide is beside you on every section, with a rope for the harder steps.",
           "O percurso atravessa as falésias por cabos de aço, degraus e algumas cordas fixas. Estás sempre preso com um kit de via ferrata com absorvedor de energia, e o guia vai contigo em todas as secções, com corda para os passos mais difíceis."),
          ("It is very exposed and very beautiful. It suits active adults and teenagers who feel fine with heights and can walk and scramble for 3 to 4 hours.",
           "É muito aéreo e muito bonito. É indicado para adultos e jovens activos que se sintam bem nas alturas e aguentem 3 a 4 horas a caminhar e trepar.")],
   included=[("Guide on every section","Guia em todas as secções"),("Harness, helmet and via ferrata lanyard set (EN 958)","Arnês, capacete e kit de via ferrata (EN 958)"),("Via ferrata gloves","Luvas de via ferrata"),("Rope and kit for short belays on hard steps","Corda e material para os passos mais difíceis"),("Activity insurance","Seguro de actividade")],
   plan=[(("Meet","Encontro"),("Welcome at the Pinheirinhos parking, safety briefing and gear fitting.","Boas-vindas no parque dos Pinheirinhos, briefing de segurança e ajuste do material.")),
         (("Approach","Aproximação"),("About 45 minutes on coastal paths down to the start.","Cerca de 45 minutos por trilhos costeiros até ao início.")),
         (("Via ferrata","Via ferrata"),("The cliff traverse, with photo stops over the sea.","A travessia da falésia, com paragens para fotos sobre o mar.")),
         (("Walk back","Regresso"),("About 40 minutes back to the parking.","Cerca de 40 minutos de volta ao parque.")),
         (("Finish","Fim"),("Gear return and debrief.","Devolução do material e conversa final."))],
   prices=[(("Shared group","Grupo partilhado"),"€65"),(("Private, 2 people (each)","Privado, 2 pessoas (cada)"),"€65"),(("Private, each extra person","Privado, cada pessoa a mais"),"€55"),(("Teens 12–15","Jovens 12–15"),"€55"),(("Solo private (total)","Privado, 1 pessoa (total)"),"€130"),(("Transfer from Lisbon, round trip","Transfer desde Lisboa, ida e volta"),"+€30"),(("Transfer from the south bank","Transfer desde a margem sul"),"+€20"),(("Full day with climbing at Forte do Cavalo","Dia inteiro com escalada no Forte do Cavalo"),"€110")],
   note=("Minimum 2 participants per departure. In summer we avoid the midday hours, and we reschedule in strong wind or rain.",
         "Mínimo de 2 participantes por saída. No verão evitamos as horas de maior calor, e reagendamos com vento forte ou chuva."),
   bring=[(("Shoes:","Calçado:"),("trail or approach shoes with good grip. No sandals.","sapatilhas de trilho com boa aderência. Nada de sandálias.")),(("Clothes:","Roupa:"),("sports clothing; a light jacket in cooler months.","desportiva; um casaco leve nos meses frios.")),(("Water:","Água:"),("1 to 1.5 L and a snack.","1 a 1,5 L e um snack.")),(("Sun:","Sol:"),("sunscreen, sunglasses and a cap.","protector solar, óculos de sol e boné.")),(("Backpack:","Mochila:"),("a small one.","uma pequena."))],
 ),
 "caminhada-arrabida": dict(
   slug="caminhada-arrabida", form_value="Arrábida hiking tour",
   incl_line=("per person · guide and insurance included","por pessoa · guia e seguro incluídos"),
   title_en="Hiking tour in Arrábida · Free Summit",
   meta_en="Guided half-day hike in the Serra da Arrábida Natural Park, near Lisbon. Ridges, sea views and Mediterranean scrub. Guide and insurance included. €35 per person.",
   place="Arrábida", coords="38.48° N, 8.98° W",
   h1=("Hike the Serra da Arrábida", "Caminhada na Serra da Arrábida"),
   sub=("A guided half-day walk where the mountains meet the sea, 45 minutes from Lisbon. Limestone ridges, wild herbs and views over the turquoise water of Portinho.",
        "Uma caminhada guiada de meio-dia onde a serra encontra o mar, a 45 minutos de Lisboa. Cumeadas de calcário, ervas aromáticas e vistas sobre a água turquesa do Portinho."),
   price="€35",
   facts=[(("Duration","Duração"),("~4 hours","~4 horas")),(("Distance","Distância"),("~8 km","~8 km")),(("Level","Nível"),("Moderate","Moderado")),(("Min. age","Idade mín."),("8 years","8 anos")),(("Group","Grupo"),("2 to 10","2 a 10"))],
   about=[("A guided hike through the Arrábida Natural Park, one of the most beautiful stretches of coast in Portugal, where green limestone hills drop straight into a clear, turquoise sea.",
           "Uma caminhada guiada pelo Parque Natural da Arrábida, um dos troços de costa mais bonitos de Portugal, onde as serras verdes de calcário caem directamente sobre um mar azul-turquesa."),
          ("We climb gently up to the ridge viewpoints, with the Tróia peninsula and the Sado estuary on one side and the open Atlantic on the other, then walk back through Mediterranean scrub full of rosemary, thyme and wild olive.",
           "Subimos com calma até aos miradouros da serra, com a península de Tróia e o estuário do Sado de um lado e o Atlântico do outro, e regressamos pelo mato mediterrânico, cheio de alecrim, tomilho e zambujeiros."),
          ("Your guide tells you about the park's plants, geology and history along the way. No technical gear needed: just good shoes and a normal level of fitness.",
           "Pelo caminho, o guia fala-te das plantas, da geologia e da história do parque. Não precisas de material técnico: só de bom calçado e de uma forma física normal.")],
   included=[("Guide who knows the park's nature and history","Guia que conhece a natureza e a história do parque"),("Route planning and timing for the weather","Escolha do percurso e do horário conforme o tempo"),("Activity insurance","Seguro de actividade"),("First aid kit","Kit de primeiros socorros")],
   plan=[(("Meet","Encontro"),("Welcome and a short briefing at the trailhead.","Boas-vindas e um briefing curto no início do trilho.")),
         (("Up to the ridge","Subida à serra"),("A steady climb to the first viewpoints over the coast.","Uma subida tranquila até aos primeiros miradouros sobre a costa.")),
         (("Along the top","Pela cumeada"),("The best views of the day, with a snack stop.","As melhores vistas do dia, com paragem para o lanche.")),
         (("Down through the scrub","Descida pelo mato"),("A different path back through the woods and scrub.","Um caminho diferente de volta, pelo bosque e pelo mato.")),
         (("Finish","Fim"),("Back at the start after about 4 hours.","De volta ao início ao fim de cerca de 4 horas."))],
   prices=[(("Shared group","Grupo partilhado"),"€35"),(("Private, 2 people (each)","Privado, 2 pessoas (cada)"),"€35"),(("Private, each extra person","Privado, cada pessoa a mais"),"€25"),(("Children 8–15","Crianças 8–15"),"€20"),(("Solo private (total)","Privado, 1 pessoa (total)"),"€70"),(("Transfer from Lisbon, round trip","Transfer desde Lisboa, ida e volta"),"+€30"),(("Transfer from Setúbal or the south bank","Transfer desde Setúbal ou margem sul"),"+€15")],
   note=("Minimum 2 participants per departure. Best from October to June; in summer we start early to avoid the heat.",
         "Mínimo de 2 participantes por saída. Melhor de Outubro a Junho; no verão começamos cedo para fugir ao calor."),
   bring=[(("Shoes:","Calçado:"),("trail or walking shoes with good grip.","sapatilhas de trilho ou de caminhada com boa aderência.")),(("Clothes:","Roupa:"),("comfortable layers; a light jacket in cooler months.","roupa confortável por camadas; um casaco leve nos meses frios.")),(("Water:","Água:"),("1.5 L and a snack.","1,5 L e um snack.")),(("Sun:","Sol:"),("sunscreen, sunglasses and a cap.","protector solar, óculos de sol e boné.")),(("Backpack:","Mochila:"),("a small one.","uma pequena."))],
 ),
}

OTHER_LINKS = [("guia", "Rock climbing in Cascais", "Escalada em Cascais"),
               ("via-ferrata", "Via ferrata in Sesimbra", "Via ferrata em Sesimbra"),
               ("caminhada-arrabida", "Hiking in Arrábida", "Caminhada na Arrábida")]

def page(p):
    facts = "".join(f'<div><dt {t(*k)}</dt><dd {t(*v)}</dd></div>' for k, v in p["facts"])
    about = "\n".join(f'<p {t(*x)}</p>' for x in p["about"])
    incl = "\n".join(f'<li {t(*x)}</li>' for x in p["included"])
    plan = "\n".join(f'<li><b {t(*a)}</b><span {t(*b)}</span></li>' for a, b in p["plan"])
    rows = []
    for k, v in p["prices"]:
        val = f'<td {t(*v)}</td>' if isinstance(v, tuple) else f'<td>{v}</td>'
        rows.append(f'<tr><th scope="row" {t(*k)}</th>{val}</tr>')
    rows = "\n".join(rows)
    bring = "\n".join(f'<li><b {t(*a)}</b> <span {t(*b)}</span></li>' for a, b in p["bring"])
    opts = "\n".join(
        f'<option value="{v}"' + (f' data-pt="{pt}"' if pt else "") + f'>{v}</option>' for v, pt in FORM_OPTIONS)
    others = "\n".join(f'<a class="btn" href="../{s}/" {t(en, pt)}</a>' for s, en, pt in OTHER_LINKS if s != p["slug"])
    incl_line = p.get("incl_line", ("per person · guide, gear and insurance included", "por pessoa · guia, material e seguro incluídos"))
    h1en, h1pt = p["h1"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p["title_en"]}</title>
<meta name="description" content="{p["meta_en"]}">
<meta property="og:title" content="{p["title_en"]}">
<meta property="og:description" content="{p["meta_en"]}">
<meta property="og:image" content="https://freesummitpt.com/assets/og-image.png">
<meta name="theme-color" content="#ECEEBF">
<link rel="icon" href="../assets/favicon.png">
<link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body data-page="{p["slug"]}">

<header class="nav">
  <div class="wrap">
    <a class="mark" href="../" aria-label="Free Summit, all activities">FREE<br>SUMMIT</a>
    <nav class="links" aria-label="Main">
      <a href="#details" data-pt="Detalhes">Details</a>
      <a href="#pricing" data-pt="Preços">Prices</a>
      <a href="../" data-pt="Todas as actividades">All activities</a>
      <a href="#book" class="keep" data-pt="Reservar">Book</a>
      <button class="lang" id="langBtn" type="button" aria-label="Mudar para português">PT</button>
    </nav>
  </div>
</header>

<main id="top">
<section class="hero act-hero" aria-labelledby="h1">
  <svg class="topo" id="topo" aria-hidden="true" preserveAspectRatio="xMidYMid slice"></svg>
  <div class="wrap">
    <p class="place-line">{p["place"]}</p>
    <h1 class="xb" id="h1" {t(h1en, h1pt)}</h1>
    <p class="lead" {t(*p["sub"])}</p>
    <div class="hero-price"><b>{p["price"]}</b><span {t(*incl_line)}</span></div>
    <div class="btns">
      <a class="btn solid" href="#book" data-pt="Reservar">Book now</a>
      <a class="btn" href="#details" data-pt="Ver detalhes">See details</a>
    </div>
  </div>
</section>

<div class="strip">
  <div class="wrap"><dl class="facts">{facts}</dl></div>
</div>

<section id="details" class="section" aria-labelledby="about-h">
  <div class="wrap two">
    <div>
      <h2 class="xb" id="about-h" data-pt="A actividade">The activity</h2>
      <div class="prose">
{about}
      </div>
    </div>
    <div>
      <h3 class="h3" data-pt="Incluído">Included</h3>
      <ul class="ticks">
{incl}
      </ul>
    </div>
  </div>
</section>

<section id="pricing" class="section" aria-labelledby="price-h">
  <div class="wrap">
    <h2 class="xb" id="price-h" data-pt="Preços">Prices</h2>
    <table class="ptable">
      <caption class="hp" data-pt="Preços">Prices</caption>
      <tbody>
{rows}
      </tbody>
    </table>
    <p class="note" {t(*p["note"])}</p>
  </div>
</section>

<section id="day" class="section" aria-labelledby="day-h">
  <div class="wrap split">
    <div>
      <h2 class="h3" id="day-h" data-pt="O plano">The plan</h2>
      <ol class="timeline">
{plan}
      </ol>
    </div>
    <div>
      <h2 class="h3" data-pt="O que trazer">What to bring</h2>
      <ul class="bring">
{bring}
      </ul>
    </div>
  </div>
</section>

<section id="book" class="book" aria-labelledby="book-h">
  <div class="wrap book-grid">
    <div>
      <h2 class="xb" id="book-h" data-pt="Reservar">Book a trip</h2>
      <p class="lede" data-pt="Diz-nos a data e quantas pessoas são. Respondemos em 24 horas com a disponibilidade e o preço final.">Tell us the date and how many of you there are. We reply within 24 hours with availability and the final price.</p>
      <div class="direct">
        <p><span data-pt="Email:">Email:</span> <a id="mailLink" href="mailto:admin@freesummitpt.com">admin@freesummitpt.com</a></p>
        <p>Instagram: <a href="https://instagram.com/freesummitpt" rel="noopener" target="_blank">@freesummitpt</a></p>
      </div>
    </div>

    <form id="bookForm" data-activity="{p["form_value"]}" novalidate>
      <div><label for="f-name" data-pt="Nome">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
      <div><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
      <div><label for="f-phone"><span data-pt="Telefone / WhatsApp">Phone / WhatsApp</span> <span class="opt" data-pt="(opcional)">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div>
        <label for="f-activity" data-pt="Actividade">Activity</label>
        <select id="f-activity" name="activity" required>
{opts}
        </select>
      </div>
      <div><label for="f-date" data-pt="Data preferida">Preferred date</label><input id="f-date" name="date" type="date"></div>
      <div><label for="f-people" data-pt="Número de pessoas">Number of people</label><input id="f-people" name="people" type="number" min="1" max="10" value="2" inputmode="numeric"></div>
      <fieldset class="full">
        <legend data-pt="Tipo de reserva">Booking type</legend>
        <div class="seg">
          <label><input type="radio" name="type" value="Shared group" checked> <span data-pt="Grupo partilhado">Shared group</span></label>
          <label><input type="radio" name="type" value="Private"> <span data-pt="Privado">Private</span></label>
        </div>
      </fieldset>
      <div class="full">
        <label for="f-transfer" data-pt="Transfer">Transfer</label>
        <select id="f-transfer" name="transfer">
          <option value="No transfer" data-pt="Não, vou ter ao ponto de encontro">No, I'll meet you there</option>
          <option value="From Lisbon" data-pt="Sim, desde Lisboa">Yes, from Lisbon</option>
          <option value="From the south bank" data-pt="Sim, desde a margem sul">Yes, from the south bank</option>
          <option value="Cascais station pick-up" data-pt="Recolha na estação de Cascais">Pick-up at Cascais station</option>
          <option value="Private transfer" data-pt="Transfer privado">Private transfer</option>
        </select>
      </div>
      <div class="full"><label for="f-msg"><span data-pt="Mensagem">Message</span> <span class="opt" data-pt="(opcional)">(optional)</span></label><textarea id="f-msg" name="message" data-pt-placeholder="Experiência, idades das crianças, horário preferido…" placeholder="Experience, children's ages, morning or afternoon…"></textarea></div>
      <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
      <div class="full"><button class="btn" type="submit" id="sendBtn" data-pt="Enviar pedido">Send request</button></div>
      <p class="form-msg" id="formMsg" role="status" aria-live="polite"></p>
      <p class="fine" data-pt="Usamos os teus dados apenas para responder a este pedido.">We only use your details to reply to this request.</p>
    </form>
  </div>
</section>

<section class="more" aria-labelledby="more-h">
  <div class="wrap">
    <h2 class="h3" id="more-h" data-pt="Mais actividades">More activities</h2>
    <div class="others">
{others}
<a class="btn solid" href="../#climbing" data-pt="Ver todas">See all</a>
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <span class="badge"><img src="../assets/fs-logo-cream.png" alt="Free Summit, go beyond." width="328" height="453"></span>
    <div class="meta">
      <div><a href="https://instagram.com/freesummitpt" rel="noopener" target="_blank">@freesummitpt</a></div>
      <!-- TODO: add your RNAAT number once registered -->
      <div>RNAAT n.º <span id="rnaat">—</span></div>
      <div>© <span id="yr">2026</span> Free Summit</div>
    </div>
  </div>
</footer>

<script src="../assets/config.js"></script>
<script src="../assets/main.js"></script>
</body>
</html>
"""

for slug, p in PAGES.items():
    os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
    path = os.path.join(ROOT, slug, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(page(p))
    print("wrote", path)
