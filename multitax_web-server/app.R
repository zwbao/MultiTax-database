library(shiny)
library(bs4Dash)

# Read full annotation file
anno <- read.delim("./other_uc_dict_human_anno.tsv")

# Define UI interface
ui <- bs4DashPage(
  header = bs4DashNavbar(
    brand = "DNA Sequence Alignment",
    color = "primary"
  ),
  sidebar = bs4DashSidebar(
    bs4DashSidebarMenu(
      bs4SidebarMenuItem("Alignment", tabName = "compare", icon = "search")
    )
  ),
  body = bs4DashBody(
    bs4DashControlbar(
      textAreaInput("sequence", "Input sequence", rows = 5),
      bs4DashActionLink("compareBtn", "Search", icon = "search", color = "primary")
    ),
    tabItems(
      tabItem(tabName = "compare",
              bs4DashBox(
                tableOutput("resultTable"),
                tableOutput("resultTable_tax"),
                color = "primary"
              )
      )
    )
  )
)

server <- function(input, output) {
  observeEvent(input$compareBtn, {
    if (!is.null(input$sequence)) {
      # Save the sequence to a temporary file
      tmpFile <- tempfile(fileext = ".fasta")
      writeLines(paste(">Query", input$sequence), tmpFile)
      
      # Execute usearch_global command for alignment, save results to a temporary file
      resultFile <- tempfile(fileext = ".txt")
      command <- paste("./usearch11.0.667_i86linux64 -usearch_global", tmpFile, "-db /home/rstudio/merged_human_all.udb -maxaccepts 0 -maxrejects 0 -top_hit_only -strand both -id 0 -blast6out", resultFile)
      system(command)
      
      result <- read.delim(resultFile, header = FALSE)
      
      r_name <- result$V2
      r_iden <- result$V3
      
      tmp <- t(anno[anno$index == r_name,-1])
      df_clean <- tmp[tmp[,1] != "",]
      df_clean <- subset(df_clean, !duplicated(df_clean))
      
      output$resultTable <- renderTable({
        result
      })
      
      output$resultTable_tax <- renderTable({
        df_clean
      })
      
    } else {
      output$resultTable <- renderText({
        "Please select a database file and input a sequence"
      })
    }
  })
}

shinyApp(ui = ui, server = server)
