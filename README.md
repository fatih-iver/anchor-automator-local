# Anchor Automator (Local)

This tool helps to publish YouTube videos as podcasts on Anchor.fm.


## Usage

Just run the following command. Just replace the variables.

```bash
docker run \
-e ANCHOR_EMAIL={anchor_email} \
-e ANCHOR_PASSWORD={anchor_password} \
-e VIDEO_URL={video_url} \
fiver6/anchor-automator-local
```

#### Example

```bash
docker run \
-e ANCHOR_EMAIL='fatih.iver@gmail.com' \
-e ANCHOR_PASSWORD='v9M/tXWT4j)FN!#y' \
-e VIDEO_URL='https://www.youtube.com/watch?v=Y66j_BUCBMY' \
fiver6/anchor-automator-local
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
