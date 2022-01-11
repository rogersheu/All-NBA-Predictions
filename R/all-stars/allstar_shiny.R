#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

# One slider would be for date to show individual date plot_predictions

# One slider could be for current probability threshold

library(shiny)
library(lubridate)

today <- Sys.Date()


# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Tracking All-Star Probabilities"),

    fluidRow(align = "center",
      selectInput("date",
                "Date:",
                choices = seq(as_date("2021-12-01"), as_date(today), by = "day"),
                selected = as_date(today)
      )
    ),

    fluidRow(align = "center",
      plotOutput("probs", height = "9.75in", width = "12in")
    ),
    
    fluidRow(align = "center",
     sliderInput("topN", label = h3("Top Nth Players by Ensemble Probability"), min = 1, 
                 max = nrow(processing_predictions(as_date("2021-12-01"), as_date(today))), value = c(1, 10))
    ),
    
    fluidRow(align = "center",
      plotOutput("lines", height = "9.75in", width = "12in")       
    )
    
    # mainPanel(
    #   plotOutput("probs", height = "9.75in", width = "12in")
    # )
    

)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  plot_day <- reactive({
    get_top_candidates(as_date(input$date))
  })
  
  output$probs <- renderPlot({
    plot_predictions(plot_day(), input$date)
  })
  
  output$lines <- renderPlot({
    plot_predictions_fixedsubset(as_date("2021-12-01"), as_date(today), input$topN)
  })
}

# Run the application 
shinyApp(ui = ui, server = server)
