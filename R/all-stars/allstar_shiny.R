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
                choices = seq(as_date(today), as_date("2021-12-01"), by = "day"),
                selected = as_date(today)
      )
    ),

    
    
    mainPanel(
      plotOutput("probs", height = "1000", width = "1000")
    )
    
        
    # Sidebar with a slider input for date alternative
    # sidebarLayout(
    #     sidebarPanel(
    #         sliderInput("date",
    #                     "Date:",
    #                     min = as_date("2021-12-01"),
    #                     max = as_date(today),
    #                     value = as_date(today))
    #     ),
    # 
    #     # Show a plot of the generated distribution
    #     mainPanel(
    #        plotOutput("probs")
    #     )
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
}

# Run the application 
shinyApp(ui = ui, server = server)
