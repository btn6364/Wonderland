#########################
# A CUSTOM URL SHORTENER
#########################


class URL_Shortener:
    def __init__(self):
        self.url_dict = {}
        self.id = 10000000000

    def shorten_url(self, origin_url):
        # use origin_url as a key
        if origin_url in self.url_dict:
            # if the key alreay exists, use it right away
            new_id = self.url_dict[origin_url]
            shorten_url = self.encode(new_id)
        else:
            self.url_dict[origin_url] = self.id
            shorten_url = self.encode(self.id)
            self.id += 1

        return "wonderland.com/" + shorten_url

    def encode(self, id):
        # base 62 characters
        characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        base = len(characters)
        encoded_url = []
        while id > 0:
            index = id % base
            encoded_url.append(characters[index])
            id = id // base
        return "".join(encoded_url[::-1])


