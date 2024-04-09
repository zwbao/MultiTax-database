argonHeader <- argonDashHeader(
  gradient = TRUE,
  color = "primary",
  separator = TRUE,
  separator_color = "secondary",
  argonCard(
    title = "Input sequence",
    hover_lift = TRUE,
    shadow = TRUE,
    shadow_size = NULL,
    hover_shadow = FALSE,
    border_level = 0,
    icon = argonIcon("fa-duotone fa-dna"),
    status = "primary",
    background_color = NULL,
    gradient = TRUE, 
    floating = FALSE,
    width = 10,
    tags$style(".form-group.shiny-input-container { width: 600px; }"),
    
    textAreaInput(
      inputId = "txt", 
      label = ""
    )
  )
)