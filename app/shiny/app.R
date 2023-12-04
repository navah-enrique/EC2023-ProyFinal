library(shiny)
library(tidyverse)
library(httr)
library(jsonlite)
library(DT)
library(plotly)
library(leaflet)
library(RColorBrewer)

dff<-read.csv("/data/venues_kmeans.csv")
Category<-unique(dff$Venue_Category)
Cluster<-unique(dff$Cluster_Labels)

# Define UI for application
ui <- fluidPage(
  tags$head(
    tags$style(
      HTML("
        .title-centering {
          text-align: center;
        }
      ")
    )
  ),
  titlePanel("Establecimientos populares y en donde encontrarlos"), 
  
  HTML("<hr>"),
  
  # Sidebar layout with input and output definitions ----
  sidebarLayout(
    sidebarPanel(
      selectInput("Values","Seleccione el tipo de establecimiento",Category, multiple = TRUE),
      HTML("<hr>"),
      selectInput("Clusters","Seleccione el Cluster",Cluster, multiple = TRUE)
    ),
    # Show map
    mainPanel(
      leafletOutput("map"),
      HTML("<hr>"),
      leafletOutput("neighborhoodMap")
    )
  )
)

server <- function(input, output) {
  filteredDataMap <- reactive({
    # Filter data based on selected Values
    dfaux <- dff %>% 
      filter(Venue_Category %in% input$Values)

    # Return the filtered data for the "map"
    return(dfaux)
  })

  filteredDataNeighborhood <- reactive({
    # Filter data based on selected Clusters
    dfaux_neighborhood <- dff %>%
      select(Neighborhood, Neighborhood_Latitude, Neighborhood_Longitude, Cluster_Labels) %>%
      distinct() %>%
      filter(Cluster_Labels %in% input$Clusters)

    # Return the filtered data for the "neighborhoodMap"
    return(dfaux_neighborhood)
  })

  output$map <- renderLeaflet({
    if (!is.null(filteredDataMap())) {
      dfaux <- filteredDataMap()
      unique_categories <- unique(dfaux$Venue_Category)
      color_palette <- colorRampPalette(brewer.pal(12, "Set3"))(length(unique_categories))

      leaflet(data = dfaux) %>%
        addTiles() %>%
        addCircleMarkers(
          lat = ~Neighborhood_Latitude,
          lng = ~Neighborhood_Longitude,
          color = ~Venue_Category,
          radius = 5,
          fillOpacity = 0.7,
          fillColor = ~factor(Venue_Category, levels = unique_categories, labels = color_palette),
          popup = ~Venue
        ) %>%
        addLegend(
          position = "bottomright",
          colors = color_palette,
          labels = unique_categories,
          title = "Tipo de Establecimientos"
        )
    }
  })

  output$neighborhoodMap <- renderLeaflet({
    if (!is.null(filteredDataNeighborhood())) {
      dfaux_neighborhood <- filteredDataNeighborhood()
      unique_clusters <- unique(dfaux_neighborhood$Cluster_Labels)
      color_palette_cluster <- colorRampPalette(brewer.pal(12, "Set3"))(length(unique_clusters))

      leaflet(data = dfaux_neighborhood) %>%
        addTiles() %>%
        addCircleMarkers(
          lat = ~Neighborhood_Latitude,
          lng = ~Neighborhood_Longitude,
          color = ~Cluster_Labels,
          radius = 5,
          fillOpacity = 0.7,
          fillColor = ~factor(Cluster_Labels, levels = unique_clusters, labels = color_palette_cluster),
          popup = ~Neighborhood
        ) %>%
        addLegend(
          position = "bottomright",
          colors = color_palette_cluster,
          labels = unique_clusters,
          title = "Clusters"
        )
    }
  })
}

# Run the application 
shinyApp(ui = ui, server = server)