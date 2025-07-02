
#import "@preview/fontawesome:0.5.0": fa-icon

#let name = "Nigel Nuique"
#let locale-catalog-page-numbering-style = context { "Nigel Nuique - Page " + str(here().page()) + " of " + str(counter(page).final().first()) + "" }
#let locale-catalog-last-updated-date-style = "Last updated in July 2025"
#let locale-catalog-language = "en"
#let design-page-size = "us-letter"
#let design-section-titles-font-size = 1.2em
#let design-colors-text = rgb(0, 0, 0)
#let design-colors-section-titles = rgb(0, 0, 0)
#let design-colors-last-updated-date-and-page-numbering = rgb(128, 128, 128)
#let design-colors-name = rgb(0, 0, 0)
#let design-colors-connections = rgb(0, 0, 0)
#let design-colors-links = rgb(0, 0, 0)
#let design-section-titles-font-family = "XCharter"
#let design-section-titles-bold = true
#let design-section-titles-line-thickness = 0.5pt
#let design-section-titles-font-size = 1.2em
#let design-section-titles-type = "with-parial-line"
#let design-section-titles-vertical-space-above = 0.55cm
#let design-section-titles-vertical-space-below = 0.3cm
#let design-section-titles-small-caps = false
#let design-links-use-external-link-icon = false
#let design-text-font-size = 10pt
#let design-text-leading = 0.6em
#let design-text-font-family = "XCharter"
#let design-text-alignment = "justified"
#let design-text-date-and-location-column-alignment = right
#let design-header-photo-width = 3.5cm
#let design-header-use-icons-for-connections = false
#let design-header-name-font-family = "XCharter"
#let design-header-name-font-size = 25pt
#let design-header-name-bold = false
#let design-header-connections-font-family = "XCharter"
#let design-header-vertical-space-between-name-and-connections = 0.7cm
#let design-header-vertical-space-between-connections-and-first-section = 0.7cm
#let design-header-use-icons-for-connections = false
#let design-header-horizontal-space-between-connections = 0.5cm
#let design-header-separator-between-connections = "|"
#let design-header-alignment = center
#let design-highlights-summary-left-margin = 0cm
#let design-highlights-bullet = "•"
#let design-highlights-top-margin = 0.25cm
#let design-highlights-left-margin = 0cm
#let design-highlights-vertical-space-between-highlights = 0.19cm
#let design-highlights-horizontal-space-between-bullet-and-highlights = 0.3em
#let design-entries-vertical-space-between-entries = 0.4cm
#let design-entries-date-and-location-width = 4.15cm
#let design-entries-allow-page-break-in-entries = true
#let design-entries-horizontal-space-between-columns = 0.1cm
#let design-entries-left-and-right-margin = 0cm
#let design-page-top-margin = 2cm
#let design-page-bottom-margin = 2cm
#let design-page-left-margin = 2cm
#let design-page-right-margin = 2cm
#let design-page-show-last-updated-date = true
#let design-page-show-page-numbering = false
#let design-links-underline = true
#let design-entry-types-education-entry-degree-column-width = 1cm
#let date = datetime.today()

// Metadata:
#set document(author: name, title: name + "'s CV", date: date)

// Page settings:
#set page(
  margin: (
    top: design-page-top-margin,
    bottom: design-page-bottom-margin,
    left: design-page-left-margin,
    right: design-page-right-margin,
  ),
  paper: design-page-size,
  footer: if design-page-show-page-numbering {
    text(
      fill: design-colors-last-updated-date-and-page-numbering,
      align(center, [_#locale-catalog-page-numbering-style _]),
      size: 0.9em,
    )
  } else {
    none
  },
  footer-descent: 0% - 0.3em + design-page-bottom-margin / 2,
)
// Text settings:
#let justify
#let hyphenate
#if design-text-alignment == "justified" {
  justify = true
  hyphenate = true
} else if design-text-alignment == "left" {
  justify = false
  hyphenate = false
} else if design-text-alignment == "justified-with-no-hyphenation" {
  justify = true
  hyphenate = false
}
#set text(
  font: design-text-font-family,
  size: design-text-font-size,
  lang: locale-catalog-language,
  hyphenate: hyphenate,
  fill: design-colors-text,
  // Disable ligatures for better ATS compatibility:
  ligatures: true,
)
#set par(
  spacing: 0pt,
  leading: design-text-leading,
  justify: justify,
)
#set enum(
  spacing: design-entries-vertical-space-between-entries,
)

// Highlights settings:
#let highlights(..content) = {
  list(
    ..content,
    marker: design-highlights-bullet,
    spacing: design-highlights-vertical-space-between-highlights,
    indent: design-highlights-left-margin,
    body-indent: design-highlights-horizontal-space-between-bullet-and-highlights,
  )
}
#show list: set list(
  marker: design-highlights-bullet,
  spacing: 0pt,
  indent: 0pt,
  body-indent: design-highlights-horizontal-space-between-bullet-and-highlights,
)

// Entry utilities:
#let three-col(
  left-column-width: 1fr,
  middle-column-width: 1fr,
  right-column-width: design-entries-date-and-location-width,
  left-content: "",
  middle-content: "",
  right-content: "",
  alignments: (auto, auto, auto),
) = [
  #block(
    grid(
      columns: (left-column-width, middle-column-width, right-column-width),
      column-gutter: design-entries-horizontal-space-between-columns,
      align: alignments,
      ([#set par(spacing: design-text-leading); #left-content]),
      ([#set par(spacing: design-text-leading); #middle-content]),
      ([#set par(spacing: design-text-leading); #right-content]),
    ),
    breakable: true,
    width: 100%,
  )
]

#let two-col(
  left-column-width: 1fr,
  right-column-width: design-entries-date-and-location-width,
  left-content: "",
  right-content: "",
  alignments: (auto, auto),
  column-gutter: design-entries-horizontal-space-between-columns,
) = [
  #block(
    grid(
      columns: (left-column-width, right-column-width),
      column-gutter: column-gutter,
      align: alignments,
      ([#set par(spacing: design-text-leading); #left-content]),
      ([#set par(spacing: design-text-leading); #right-content]),
    ),
    breakable: true,
    width: 100%,
  )
]

// Main heading settings:
#let header-font-weight
#if design-header-name-bold {
  header-font-weight = 700
} else {
  header-font-weight = 400
}
#show heading.where(level: 1): it => [
  #set par(spacing: 0pt)
  #set align(design-header-alignment)
  #set text(
    font: design-header-name-font-family,
    weight: header-font-weight,
    size: design-header-name-font-size,
    fill: design-colors-name,
  )
  #it.body
  // Vertical space after the name
  #v(design-header-vertical-space-between-name-and-connections)
]

#let section-title-font-weight
#if design-section-titles-bold {
  section-title-font-weight = 700
} else {
  section-title-font-weight = 400
}

#show heading.where(level: 2): it => [
  #set align(left)
  #set text(size: (1em / 1.2)) // reset
  #set text(
    font: design-section-titles-font-family,
    size: (design-section-titles-font-size),
    weight: section-title-font-weight,
    fill: design-colors-section-titles,
  )
  #let section-title = (
    if design-section-titles-small-caps [
      #smallcaps(it.body)
    ] else [
      #it.body
    ]
  )
  // Vertical space above the section title
  #v(design-section-titles-vertical-space-above, weak: true)
  #block(
    breakable: false,
    width: 100%,
    [
      #if design-section-titles-type == "moderncv" [
        #two-col(
          alignments: (right, left),
          left-column-width: design-entries-date-and-location-width,
          right-column-width: 1fr,
          left-content: [
            #align(horizon, box(width: 1fr, height: design-section-titles-line-thickness, fill: design-colors-section-titles))
          ],
          right-content: [
            #section-title
          ]
        )

      ] else [
        #box(
          [
            #section-title
            #if design-section-titles-type == "with-parial-line" [
              #box(width: 1fr, height: design-section-titles-line-thickness, fill: design-colors-section-titles)
            ] else if design-section-titles-type == "with-full-line" [

              #v(design-text-font-size * 0.4)
              #box(width: 1fr, height: design-section-titles-line-thickness, fill: design-colors-section-titles)
            ]
          ]
        )
      ]
     ] + v(1em),
  )
  #v(-1em)
  // Vertical space after the section title
  #v(design-section-titles-vertical-space-below - 0.5em)
]

// Links:
#let original-link = link
#let link(url, body) = {
  body = [#if design-links-underline [#underline(body)] else [#body]]
  body = [#if design-links-use-external-link-icon [#body#h(design-text-font-size/4)#box(
        fa-icon("external-link", size: 0.7em),
        baseline: -10%,
      )] else [#body]]
  body = [#set text(fill: design-colors-links);#body]
  original-link(url, body)
}

// Last updated date text:
#if design-page-show-last-updated-date {
  let dx
  if design-section-titles-type == "moderncv" {
    dx = 0cm
  } else {
    dx = -design-entries-left-and-right-margin
  }
  place(
    top + right,
    dy: -design-page-top-margin / 2,
    dx: dx,
    text(
      [_#locale-catalog-last-updated-date-style _],
      fill: design-colors-last-updated-date-and-page-numbering,
      size: 0.9em,
    ),
  )
}

#let connections(connections-list) = context {
  set text(fill: design-colors-connections, font: design-header-connections-font-family)
  set par(leading: design-text-leading*1.7, justify: false)
  let list-of-connections = ()
  let separator = (
    h(design-header-horizontal-space-between-connections / 2, weak: true)
      + design-header-separator-between-connections
      + h(design-header-horizontal-space-between-connections / 2, weak: true)
  )
  let starting-index = 0
  while (starting-index < connections-list.len()) {
    let left-sum-right-margin
    if type(page.margin) == "dictionary" {
      left-sum-right-margin = page.margin.left + page.margin.right
    } else {
      left-sum-right-margin = page.margin * 4
    }

    let ending-index = starting-index + 1
    while (
      measure(connections-list.slice(starting-index, ending-index).join(separator)).width
        < page.width - left-sum-right-margin
    ) {
      ending-index = ending-index + 1
      if ending-index > connections-list.len() {
        break
      }
    }
    if ending-index > connections-list.len() {
      ending-index = connections-list.len()
    }
    list-of-connections.push(connections-list.slice(starting-index, ending-index).join(separator))
    starting-index = ending-index
  }
  align(list-of-connections.join(linebreak()), design-header-alignment)
  v(design-header-vertical-space-between-connections-and-first-section - design-section-titles-vertical-space-above)
}

#let three-col-entry(
  left-column-width: 1fr,
  right-column-width: design-entries-date-and-location-width,
  left-content: "",
  middle-content: "",
  right-content: "",
  alignments: (left, auto, right),
) = (
  if design-section-titles-type == "moderncv" [
    #three-col(
      left-column-width: right-column-width,
      middle-column-width: left-column-width,
      right-column-width: 1fr,
      left-content: right-content,
      middle-content: [
        #block(
          [
            #left-content
          ],
          inset: (
            left: design-entries-left-and-right-margin,
            right: design-entries-left-and-right-margin,
          ),
          breakable: design-entries-allow-page-break-in-entries,
          width: 100%,
        )
      ],
      right-content: middle-content,
      alignments: (design-text-date-and-location-column-alignment, left, auto),
    )
  ] else [
    #block(
      [
        #three-col(
          left-column-width: left-column-width,
          right-column-width: right-column-width,
          left-content: left-content,
          middle-content: middle-content,
          right-content: right-content,
          alignments: alignments,
        )
      ],
      inset: (
        left: design-entries-left-and-right-margin,
        right: design-entries-left-and-right-margin,
      ),
      breakable: design-entries-allow-page-break-in-entries,
      width: 100%,
    )
  ]
)

#let two-col-entry(
  left-column-width: 1fr,
  right-column-width: design-entries-date-and-location-width,
  left-content: "",
  right-content: "",
  alignments: (auto, design-text-date-and-location-column-alignment),
  column-gutter: design-entries-horizontal-space-between-columns,
) = (
  if design-section-titles-type == "moderncv" [
    #two-col(
      left-column-width: right-column-width,
      right-column-width: left-column-width,
      left-content: right-content,
      right-content: [
        #block(
          [
            #left-content
          ],
          inset: (
            left: design-entries-left-and-right-margin,
            right: design-entries-left-and-right-margin,
          ),
          breakable: design-entries-allow-page-break-in-entries,
          width: 100%,
        )
      ],
      alignments: (design-text-date-and-location-column-alignment, auto),
    )
  ] else [
    #block(
      [
        #two-col(
          left-column-width: left-column-width,
          right-column-width: right-column-width,
          left-content: left-content,
          right-content: right-content,
          alignments: alignments,
        )
      ],
      inset: (
        left: design-entries-left-and-right-margin,
        right: design-entries-left-and-right-margin,
      ),
      breakable: design-entries-allow-page-break-in-entries,
      width: 100%,
    )
  ]
)

#let one-col-entry(content: "") = [
  #let left-space = design-entries-left-and-right-margin
  #if design-section-titles-type == "moderncv" [
    #(left-space = left-space + design-entries-date-and-location-width + design-entries-horizontal-space-between-columns)
  ]
  #block(
    [#set par(spacing: design-text-leading); #content],
    breakable: design-entries-allow-page-break-in-entries,
    inset: (
      left: left-space,
      right: design-entries-left-and-right-margin,
    ),
    width: 100%,
  )
]

= Nigel Nuique

// Print connections:
#let connections-list = (
  [Melbourne, Victoria],
  [#box(original-link("mailto:nigelnuique@gmail.com")[nigelnuique\@gmail.com])],
  [#box(original-link("tel:+61-435-395-191")[0435 395 191])],
  [#box(original-link("https://nigelnuique.com/")[nigelnuique.com])],
  [#box(original-link("https://linkedin.com/in/nigelnuique")[linkedin.com\/in\/nigelnuique])],
  [#box(original-link("https://github.com/nigelnuique")[github.com\/nigelnuique])],
)
#connections(connections-list)



== Professional Summary


#one-col-entry(
  content: [Data professional with a background in data science, electronics engineering, and hands-on project delivery across industry and academic settings. Experienced in programming, data analysis, and prototyping, with exposure to NLP, machine learning, cloud platforms, and embedded systems. Skilled at building end-to-end solutions, from early ideation to deployment. Brings a strong mix of analytical thinking, practical problem-solving, and cross-functional collaboration in both independent and team-based environments.]
)


== Education


// YES DATE, NO DEGREE
#two-col-entry(
  left-content: [
    #strong[RMIT University], MS in Data Science -- Melbourne, Australia
  ],
  right-content: [
    Feb 2023 – Dec 2024
  ],
)
#block(
  [
    #set par(spacing: 0pt)
    #v(design-highlights-top-margin);#highlights([Academic merit scholarship],[GPA: 3.5\/4.0 \(Distinction\)],[Capstone Project: Developed an NLP pipeline to harmonise medical concepts using UMLSBERT and SciSpaCy. Used Plotly for interactive dashboards and visual validation of mappings],[Relvant Coursework: Algorithms and Analysis, Programming Fundamentals, Case Studies in Data Science, Practical Data Science with Python, The Data Science Professional, Advanced Programming for Data Science, Database Concepts, Data Wrangling, Big Data Processing, Cloud Computing, Data Science Postgraduate Project, Social Media and Networks Analytics, Computational Machine Learning, Applied Analytics, Data Visualisation and Communication ],)
  ],
  inset: (
    left: design-entries-left-and-right-margin,
    right: design-entries-left-and-right-margin,
  ),
)

#v(design-entries-vertical-space-between-entries)
// YES DATE, NO DEGREE
#two-col-entry(
  left-content: [
    #strong[University of San Carlos], BS in Electronics Engineering -- Cebu, Philippines
  ],
  right-content: [
    July 2014 – May 2019
  ],
)
#block(
  [
    #set par(spacing: 0pt)
    #v(design-highlights-top-margin);#highlights([Major in Instrummentation and Controls],[Thesis: Prepaid Solar Sytem for off Grid Communities],[Relevant Coursework: General and Inorganic Chemistry, Electronics Technology, Engineering Graphics, Calculus, Discrete Mathematics, Computer Fundamentals & Programming, Engineering Physics, Probability and Statistics, DC Circuits, Engineering Mechanics, Numerical Methods, Vector Analysis, Electronics Devices and Circuits, Engineering Materials, AC Circuits, Strength of Materials, Electronics Circuit Analysis and Design, Electromagnetics, Digital Electronics & Switching Theory, Signals, Spectra & Signal Processing, Thermodynamics, Principles of Communications, RF Circuit Analysis and Design, Feedback Control Systems, Energy Conversion, Modeling Engineering Systems, Digital Communications, Transmission Media and Antenna Systems, Microprocessor System, Computer Applications, Industrial Electronics, Embedded Controllers and Data Analysis, Fundamentals of LabVIEW, VLSI Design, Advanced Computer Programming, Data Communications, Safety Management],)
  ],
  inset: (
    left: design-entries-left-and-right-margin,
    right: design-entries-left-and-right-margin,
  ),
)



== Experience


#two-col-entry(
  left-content: [
    #strong[Personal Shopper], Woolworths Group -- Melbourne, AU
  ],
  right-content: [
    Jan 2025 – present
  ],
)
#one-col-entry(
  content: [
    #v(design-highlights-top-margin);#highlights([Fulfilled and processed online customer orders with accuracy and efficiency],[Coordinated with store teams to resolve stock issues],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #strong[Strategic Contributor], Natural Velocity -- Melbourne, AU \(Hybrid\)
  ],
  right-content: [
    June 2025 – present
  ],
)
#one-col-entry(
  content: [
    #v(design-highlights-top-margin);#highlights([Brought on for data science expertise with flexibility to support strategy, research, and operations],[Built a PowerBI dashboard that improved sales pipeline visibility and enabled prioritization of high-impact opportunities],[Contributing across initiatives in an early-stage AI and cybersecurity startup],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #strong[Transition Support Officer | Property Audit Assistant], RMIT University -- Melbourne, AU
  ],
  right-content: [
    July 2023 – Feb 2024
  ],
)
#one-col-entry(
  content: [
    #v(design-highlights-top-margin);#highlights([Conducted AV\/IT audits across 14 buildings],[Resolved 37 technical issues and updated 90+ support guides],[Ensured classrooms followed layout and cleanliness standards],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #strong[Associate Member of Technical Staff, Test Systems Development], Maxim Integrated \(acquired by Analog Devices\) -- Cavite, PH
  ],
  right-content: [
    Jan 2020 – Oct 2021
  ],
)
#one-col-entry(
  content: [
    #v(design-highlights-top-margin);#highlights([Developed hardware and software for automated IC testing],[Resolved production line issues with product engineers],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #strong[Test Development Engineer], Analog Devices -- Cavite, PH
  ],
  right-content: [
    Oct 2021 – Jan 2023
  ],
)
#one-col-entry(
  content: [
    #v(design-highlights-top-margin);#highlights([Developed test solutions and hardware for 4 new IC products],[Led qualifications for 10 products, releasing 40 setups],[Improved tester availability by 15\% by removing redundant tests],[Collaborated across QA, design, and production teams],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #strong[Casual Event Staff], Spark Event Group -- Melbourne, AU
  ],
  right-content: [
    May 2023 – Jan 2025
  ],
)
#one-col-entry(
  content: [
    #v(design-highlights-top-margin);#highlights([Supported major events including the FIFA WWC Finals, RMIT Graduation, Rotary Club International Convention, and the Australian Open],[Assisted with guest wayfinding, ticket inspection, handing out testamurs, and responding to attendee inquiries],)
  ],
)



== Projects


#two-col-entry(
  left-content: [
    #link("https://github.com/nigelnuique/clinical_notes_AI_agent")[#strong[Clinical Notes AI Agent]] 
  ],
  right-content: [
    May 2025
  ],
)
#one-col-entry(
  content: [
    #two-col(left-column-width: design-highlights-summary-left-margin, right-column-width: 1fr, left-content: [], right-content: [#v(design-highlights-top-margin);#align(left, [LangGraph-based agent that extracts and validates tasks from clinical notes])], column-gutter: 0cm)

#v(-design-text-leading)  #v(design-highlights-top-margin);#highlights([Extracts pathology, radiology, medication, and follow-up tasks],[Sends validated summaries via PDF, email, and SMS],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #link("https://public.tableau.com/app/profile/nigel.ray.nuique/viz/Book1_17389035244010/Dashboard1")[#strong[Melbourne Airbnb Tableau Dashboard]] 
  ],
  right-content: [
    Feb 2025
  ],
)
#one-col-entry(
  content: [
    #two-col(left-column-width: design-highlights-summary-left-margin, right-column-width: 1fr, left-content: [], right-content: [#v(design-highlights-top-margin);#align(left, [Visual dashboard showing geospatial pricing trends in Melbourne Airbnb market])], column-gutter: 0cm)

#v(-design-text-leading)  #v(design-highlights-top-margin);#highlights([Created a multi-filter Tableau dashboard with price heatmaps],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #link("https://nigelnuique.com/blog/running-shoe-geeks-analysis")[#strong[Running Shoe Subreddit Analysis]] 
  ],
  right-content: [
    Sept 2024
  ],
)
#one-col-entry(
  content: [
    #two-col(left-column-width: design-highlights-summary-left-margin, right-column-width: 1fr, left-content: [], right-content: [#v(design-highlights-top-margin);#align(left, [NLP analysis of shoe brand sentiment on r\/runningshoegeeks])], column-gutter: 0cm)

#v(-design-text-leading)  #v(design-highlights-top-margin);#highlights([Used Python, PRAW, and NLTK to analyse community posts and sentiment],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #link("https://github.com/nigelnuique/layoffs-data-analysis-2023-24")[#strong[Layoffs Data Analysis]] 
  ],
  right-content: [
    Nov 2024
  ],
)
#one-col-entry(
  content: [
    #two-col(left-column-width: design-highlights-summary-left-margin, right-column-width: 1fr, left-content: [], right-content: [#v(design-highlights-top-margin);#align(left, [Trend analysis of layoffs by industry and season using SQL])], column-gutter: 0cm)

#v(-design-text-leading)  #v(design-highlights-top-margin);#highlights([Cleaned ,transformed, and analysed the datasets using SQL],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #link("https://github.com/nigelnuique/user_identification_using_walking_data")[#strong[User Identification from Walking Activity Data]] 
  ],
  right-content: [
    May 2024
  ],
)
#one-col-entry(
  content: [
    #two-col(left-column-width: design-highlights-summary-left-margin, right-column-width: 1fr, left-content: [], right-content: [#v(design-highlights-top-margin);#align(left, [Used KNN and Decision Trees to identify users based on walking activity])], column-gutter: 0cm)

#v(-design-text-leading)  #v(design-highlights-top-margin);#highlights([Achieved 97\% accuracy using KNN and 93.1\% using Decision Tree],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #link("https://github.com/nigelnuique/job_search_web_app")[#strong[Job Search Web Application]] 
  ],
  right-content: [
    Dec 2023
  ],
)
#one-col-entry(
  content: [
    #two-col(left-column-width: design-highlights-summary-left-margin, right-column-width: 1fr, left-content: [], right-content: [#v(design-highlights-top-margin);#align(left, [Built a Flask app with job search and job posting functionality])], column-gutter: 0cm)

#v(-design-text-leading)  #v(design-highlights-top-margin);#highlights([Recommended job categories with 87\% accuracy using TF-IDF and NLP],)
  ],
)



== Skills


#one-col-entry(
  content: [#strong[Programming:] Python, SQL, R, Git, C++, Visual Basic, Jupyter, VSCode]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[Visualization:] Tableau, PowerBI, Plotly, matplotlib, seaborn]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[AI & ML:] LLMs \(OpenAI, HuggingFace\),Amazon Bedrock, SciSpaCy, UMLSBERT, Prompt Engineering, LangGraph,LangChain, scikit-learn, NumPy, pandas]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[Cloud:] AWS \(basic\), Google Cloud \(BigQuery, Vertex AI\), Azure]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[Tools:] Neo4j, Hadoop, Cursor, SendGrid, Twilio, Jira, Confluence, Jupyter]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[Web:] HTML, CSS, JavaScript, Flask]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[Electronics:] PCB layout \(Altium\), microcontrollers \(Arduino, STM32\), circuit design, oscilloscopes, signal generators]
)


== Certifications


#one-col-entry(
  content: [Azure Data Fundamentals DP-900]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [Google Data Analytics Professional Certificate]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [Neo4j Certified Profesional]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [Registered Electronics Engineer \(PH\)]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [Registered Electronics Technician \(PH\)]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [RSA \(VIC\)]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [Working With Children Check \(Employee\)]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [Full Victorian Driver's License]
)


== Extracurricular


#one-col-entry(
  content: [#strong[IBM Micro-Internship:] Explored Generative AI for business. Gained hands-on experience in GenAI and IBM Design Thinking]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[RMIT Global Leader Experience:] Worked in cross-disciplinary teams to design urban solutions for Melbourne]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[Volunteering:] BeerOPS VIP sign-in, Sole Motive Run Melbourne Expo, Together Campaign Team \(RMIT University Student Union Elections\), Foodbank, RUSU RealFoods Café, Yow! Conferences]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[Entrepreneurship:] Founder of dialed.cc, a cycling focused eCommerce store with 900+ followers and 99\% positive ratings on Lazada PH]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[Hobbies:] Running, Cycling]
)


