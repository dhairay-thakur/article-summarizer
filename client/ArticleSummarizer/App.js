import React, {useState} from 'react';
import {StyleSheet, View, Button, Text, TextInput, Image} from 'react-native';
import axios from 'axios';
import Share from 'react-native-share';

const App = props => {
  const [url, setUrl] = useState('');
  const [imageUri, setImageUri] = useState('');

  const shareOptions = {
    method: Share.InstagramStories.SHARE_BACKGROUND_IMAGE,
    backgroundImage: imageUri,
    backgroundBottomColor: '#fefefe',
    backgroundTopColor: '#906df4',
    social: Share.Social.INSTAGRAM_STORIES,
  };

  const handleSubmit = () => {
    console.log(url);
    axios
      .post('https://article-summarize.herokuapp.com/api', {
        url,
      })
      .then(function (response) {
        // handle success
        setImageUri('http://192.168.43.210:5000/api/get-image');
      })
      .catch(function (error) {
        // handle error
        alert(error.message);
      });
  };

  const handleShare = () => {
    Share.shareSingle(shareOptions)
      .then(res => {
        console.log(res);
      })
      .catch(err => {
        err && console.log(err);
      });
  };

  return (
    <View style={styles.background}>
      {imageUri === '' && (
        <TextInput
          style={styles.textInput}
          onChangeText={text => setUrl(text)}
        />
      )}
      {imageUri === '' && (
        <Button
          style={styles.button}
          title="Generate Summary"
          onPress={handleSubmit}
        />
      )}

      {imageUri !== '' && (
        <Image style={styles.image} source={{uri: imageUri}} />
      )}
      {imageUri === '' && (
        <Image style={styles.noImage} source={require('./no-results.png')} />
      )}
      {imageUri !== '' && (
        <Button style={styles.button} title="Share" onPress={handleShare} />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  background: {
    backgroundColor: 'white',
    padding: 20,
    flex: 1,
    alignItems: 'center',
  },
  textInput: {
    borderWidth: 1,
    borderRadius: 20,
    paddingHorizontal: 10,
    marginVertical: 10,
    backgroundColor: 'blue',
  },
  noImage: {
    marginVertical: 100,
    width: 320,
    height: 340,
  },
  image: {
    marginVertical: 10,
    width: '100%',
    height: '80%',
  },
  button: {
    marginVertical: 10,
    borderRadius: 20,
    backgroundColor: 'black',
  },
});

export default App;
