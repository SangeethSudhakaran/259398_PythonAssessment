import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import os

st.title("Streamlit  | Movie Browser APP")

option = st.selectbox(
    "Select operation",
    ("Rating","Plot","Stars","Director"),
)

data= "Test data"
movieDetails = {}

movieNameKeyword = st.text_input("Movie Keyword:")

def SearchMovie():
  try:
    # Geckodriver file path
    driver_path = os.getcwd() + '/Selenium/MozillaDriver/geckodriver.exe'

    service = Service(driver_path)
    driver = webdriver.Firefox(service=service)

    # Navigating into the URL
    driver.get("https://www.imdb.com")
    # Print title
    print("Navigating to", driver.title)

    Searchbar = driver.find_element(By.ID,"suggestion-search")
    SearchButton = driver.find_element(By.ID,"suggestion-search-button")

    print("Elements located and filing values")
    Searchbar.send_keys(movieNameKeyword)
    SearchButton.click()    
    driver.implicitly_wait(5)

    firstItemInMovieList = driver.find_element(By.XPATH,"//div[@class='ipc-metadata-list-summary-item__tc']/a")
    firstItemInMovieList.click()

    data = GetMovieDetails(d=driver)
    driver.implicitly_wait(5)
    driver.quit()
    return data
  except Exception as e:   
    print("Exception in movie search:",e) 


def GetMovieDetails(d):
    d.implicitly_wait(5)
    starsDetails=""
    stars = d.find_elements(By.XPATH,"//li[@data-testid='title-pc-principal-credit']//a[normalize-space(text())='Stars']/following-sibling::div/ul/li")
    for eachstar in stars:
      if len(eachstar.text) > 0 : starsDetails += (eachstar.text," - " + eachstar.text)[len(starsDetails)>0]

    movieDetails = {'Title' : d.find_element(By.XPATH,"//h1[@data-testid='hero__pageTitle']//span").text,
                         'Stars' : starsDetails,
                         'Rating' : d.find_element(By.XPATH,"//div[@data-testid='hero-rating-bar__aggregate-rating__score']//span").text + "/10",
                         'Director' : d.find_element(By.XPATH,"//li[@data-testid='title-pc-principal-credit']//a").text,
                         'Plot' : d.find_element(By.XPATH,"//p[@data-testid='plot']//span[@data-testid='plot-xl']").text}
    return "Movie found : " + movieDetails.get('Title') + " -- " + option + ":" + movieDetails.get(option)

if(st.button("Get movie data", type="primary")):
    if(len(movieNameKeyword)>0 and len(option)>0):
        st.write("Generating the results for movie keyword:", movieNameKeyword ,":", option)
        data = SearchMovie()
        st.write(":blue[" + data + "]")
    else:
        st.write(":red[Invalid inputs, Please check the inputs!!]")