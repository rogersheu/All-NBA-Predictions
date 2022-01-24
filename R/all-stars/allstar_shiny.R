library(shiny)
library(lubridate)

today <- Sys.Date()

### ISSUE SOMEWHERE, DEBUG

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel(h1("Tracking All-Star Probabilities", align = "center")),

    fluidRow(align = "center",
      selectInput("date",
                "Date:",
                choices = seq(as_date("2021-12-01"), as_date(today), by = "day"),
                width = "150px",
                selected = as_date(today)
                )
    ),

    fluidRow(align = "center",
      plotOutput("probs", height = "6.5in", width = "8in")
    ),
    
    fluidRow(align = "center",
     sliderInput("topN", label = h3("Top Players by Ensemble Probability"), min = 1, 
                 max = nrow(processing_predictions(as_date("2021-12-01"), as_date(today))), 
                 step = 1,
                 #ticks = FALSE, 
                 width = "400px",
                 value = c(1, 10)
                 )
    ),
    
    fluidRow(align = "center",
             actionButton("update", "Update Player Range")      
    ),
    
    fluidRow(align = "center",
      plotOutput("lines", height = "8in", width = "10in")       
    )

)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  playerRange <- eventReactive(input$update, {
    input$topN
  }, ignoreNULL = FALSE)
  
  plot_day <- reactive({
    get_top_candidates(as_date(input$date))
  })
  
  output$probs <- renderPlot({
    plot_predictions(plot_day(), input$date, FALSE)
  })
  
  output$lines <- renderPlot({
    plot_predictions_fixedsubset(as_date("2021-12-01"), as_date(today), playerRange())
  })
}

# Run the application 
shinyApp(ui = ui, server = server)
