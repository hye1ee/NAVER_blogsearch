## Install required libraries

```bash
pip install numpy pandas plotly python-dotenv wordcloud konlpy
```

<br />

## Set environment variables

Copy and fill the environment file, please refer the following details.

```bash
cp .env.example .env # Linux and macOS
copy .env.example .env # Windows
```

- To set client id and password, you need to register your application. Please refer the following [link](https://developers.naver.com/apps/#/register).

- To set JVM path, you need to check your JDK version
  ```bash
  cd /Library/Java/JavaVirtualMachines
  ls
  ```
  Choose and remember one version of the indicated list (e.g. zulu-21.jdk), set the JVM path following the format below
  ```bash
  JVM_PATH = /Library/Java/JavaVirtualMachines/${JVM_VERSION}/Contents/Home/bin/java'
  ```

<br />

## Play with demo

Get the Naver blog search data and the wordcloud result with following command.

```bash
python word*cloud.py --query ${QUERY} --filename ${FILE_NAME} --count ${COUNT}
```

- **${QUERY}** is the Naver blog search query. No restriction for the query.
- **${FILE_NAME}** is the name of result files, it is allowed to contains only alphabets and underbar symbol(\_).
- **${COUNT}** is the criteria number of generating word cloud. The words which appeared more thatn COUNT times will be displayed in the word cloud image.

```bash
# example command
python word_cloud.py --query "재테크" --filename "invest" --count 100
```

The word cloud is generated based on the title and the description of each contents.
The JSON data from API request and the image of wordcloud will be stored at `data/`.
