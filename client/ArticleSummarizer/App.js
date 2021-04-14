import React, {useState} from 'react';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  Image,
  TouchableOpacity,
} from 'react-native';
import axios from 'axios';
import RNStoryShare from 'react-native-story-share';

const BASE_URL = 'https://article-summarize.herokuapp.com/api';

const App = props => {
  const [url, setUrl] = useState('');
  const [imageId, setImageId] = useState(null);

  const deleteImage = () => {
    axios
      .post(`${BASE_URL}/remove-image/${imageId}`)
      .then(function (response) {
        // handle success
        console.log(response.data);
      })
      .catch(function (error) {
        // handle error
        console.log(error.message);
      });
  };

  const handleSubmit = () => {
    console.log(url);
    axios
      .post(BASE_URL, {
        url,
      })
      .then(function (response) {
        // handle success
        console.log(response.data.imageId);
        setImageId(response.data.imageId);
      })
      .catch(function (error) {
        // handle error
        alert(error.message);
      });
  };

  const handleShare = () => {
    RNStoryShare.isInstagramAvailable()
      .then(isAvailable => {
        if (isAvailable) {
          RNStoryShare.shareToInstagram({
            type: RNStoryShare.FILE, // or RNStoryShare.FILE
            backgroundAsset: imageId,
            backgroundBottomColor: '#f44162',
            backgroundTopColor: '#f4a142',
          });
        }
      })
      .catch(e => console.log(e));
  };

  const handleReset = () => {
    deleteImage();
    setImageId(null);
    setUrl('');
  };

  return (
    <View style={styles.background}>
      {!imageId && (
        <TextInput
          placeholder="Link to the Article"
          placeholderTextColor="#1f2833"
          selectionColor="#66fcf1"
          style={styles.textInput}
          onChangeText={text => setUrl(text)}
        />
      )}
      {!imageId && (
        <TouchableOpacity style={styles.button} onPress={handleSubmit}>
          <Text style={styles.btnText}>Generate Summary</Text>
        </TouchableOpacity>
      )}
      {imageId && (
        <Image
          style={styles.image}
          source={{uri: `${BASE_URL}/get-image/${imageId}`}}
        />
      )}
      {!imageId && (
        <Image style={styles.noImage} source={require('./no-results.png')} />
      )}
      {imageId && (
        <TouchableOpacity style={styles.button} onPress={handleShare}>
          <Text style={styles.btnText}>Share Story</Text>
        </TouchableOpacity>
      )}
      {imageId && (
        <TouchableOpacity style={styles.button} onPress={handleReset}>
          <Text style={styles.btnText}>Reset</Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  background: {
    backgroundColor: '#1f2833',
    padding: 20,
    flex: 1,
    alignItems: 'center',
  },
  textInput: {
    width: 300,
    borderWidth: 1,
    paddingHorizontal: 10,
    borderRadius: 50,
    marginVertical: 10,
    color: '#0b0c10',
    backgroundColor: '#c5c6c7',
  },
  noImage: {
    marginVertical: 100,
    width: 320,
    height: 340,
  },
  image: {
    marginVertical: 10,
    width: '100%',
    height: '75%',
  },
  button: {
    width: 250,
    marginTop: 10,
    borderWidth: 1,
    borderColor: '#66fcf1',
    padding: 15,
    borderRadius: 50,
  },
  btnText: {
    color: '#66fcf1',
    fontSize: 18,
    justifyContent: 'center',
    textAlign: 'center',
  },
});

export default App;
