author_valid = 'Tolkien'
author_invalid = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
start_index_invalid = '&startIndex=x'
json_input_valid = {
  "kind": "books#volumes",
  "totalItems": 197,
  "items": [
    {
      "kind": "books#volume",
      "id": "ti3Qbej5wg4C",
      "etag": "udcy889G+F4",
      "selfLink": "https://www.googleapis.com/books/v1/volumes/ti3Qbej5wg4C",
      "volumeInfo": {
        "title": "Interesting Times",
        "subtitle": "(Discworld Novel 17)",
        "authors": [
          "Terry Pratchett"
        ],
        "publisher": "Random House",
        "publishedDate": "2008-12-05",
        "description": "‘Funny, delightfully inventive, and refuses to lie down in its genre’ Observer The Discworld is very much like our own – if our own were to consist of a flat planet balanced on the back of four elephants which stand on the back of a giant turtle, that is . . . There is a curse. They say: may you live in interesting times. ’May you live in interesting times’ is the worst thing one can wish on a citizen of Discworld, especially on the distinctly unmagical Rincewind, who has had far too much perilous excitement in his life and can’t even spell wizard. So when a request for a ;Great Wizzard; arrives in Ankh-Morpork via carrier albatross from the faraway Counterweight Continent, it's the endlessly unlucky Rincewind who's sent as emissary. The oldest (and most heavily fortified) empire on the Disc is in turmoil, and Chaos is building. And, for some incomprehensible reason, someone believes Rincewind will have a mythic role in the ensuing war and wholesale bloodletting. There are too many heroes already in the world, but there is only one Rincewind. And he owes it to the world to keep that one alive for as long as possible. ____________________ The Discworld novels can be read in any order but Interesting Times is the fifth book in the Wizards series.",
        "industryIdentifiers": [
          {
            "type": "ISBN_13",
            "identifier": "9781407034966"
          },
          {
            "type": "ISBN_10",
            "identifier": "1407034960"
          }
        ],
        "readingModes": {
          "text": 'true',
          "image": 'false'
        },
        "pageCount": 432,
        "printType": "BOOK",
        "categories": [
          "Fiction"
        ],
        "averageRating": 3.5,
        "ratingsCount": 34,
        "maturityRating": "NOT_MATURE",
        "allowAnonLogging": 'true',
        "contentVersion": "4.21.13.0.preview.2",
        "panelizationSummary": {
          "containsEpubBubbles": 'false',
          "containsImageBubbles": 'false'
        },
        "imageLinks": {
          "smallThumbnail": "http://books.google.com/books/content?id=ti3Qbej5wg4C&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api",
          "thumbnail": "http://books.google.com/books/content?id=ti3Qbej5wg4C&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"
        },
        "language": "en",
        "previewLink": "http://books.google.pl/books?id=ti3Qbej5wg4C&printsec=frontcover&dq=inauthor:Pratchett&hl=&cd=2&source=gbs_api",
        "infoLink": "https://play.google.com/store/books/details?id=ti3Qbej5wg4C&source=gbs_api",
        "canonicalVolumeLink": "https://play.google.com/store/books/details?id=ti3Qbej5wg4C"
      },
      "saleInfo": {
        "country": "PL",
        "saleability": "FOR_SALE",
        "isEbook": 'true',
        "listPrice": {
          "amount": 37.99,
          "currencyCode": "PLN"
        },
        "retailPrice": {
          "amount": 37.99,
          "currencyCode": "PLN"
        },
        "buyLink": "https://play.google.com/store/books/details?id=ti3Qbej5wg4C&rdid=book-ti3Qbej5wg4C&rdot=1&source=gbs_api",
        "offers": [
          {
            "finskyOfferType": 1,
            "listPrice": {
              "amountInMicros": 37990000,
              "currencyCode": "PLN"
            },
            "retailPrice": {
              "amountInMicros": 37990000,
              "currencyCode": "PLN"
            }
          }
        ]
      },
      "accessInfo": {
        "country": "PL",
        "viewability": "PARTIAL",
        "embeddable": 'true',
        "publicDomain": 'false',
        "textToSpeechPermission": "ALLOWED",
        "epub": {
          "isAvailable": 'true',
          "acsTokenLink": "http://books.google.pl/books/download/Interesting_Times-sample-epub.acsm?id=ti3Qbej5wg4C&format=epub&output=acs4_fulfillment_token&dl_type=sample&source=gbs_api"
        },
        "pdf": {
          "isAvailable": 'false'
        },
        "webReaderLink": "http://play.google.com/books/reader?id=ti3Qbej5wg4C&hl=&printsec=frontcover&source=gbs_api",
        "accessViewStatus": "SAMPLE",
        "quoteSharingAllowed": 'false'
      },
      "searchInfo": {
        "textSnippet": "And he owes it to the world to keep that one alive for as long as possible. ____________________ The Discworld novels can be read in any order but Interesting Times is the fifth book in the Wizards series."
      }
    }]}

json_input_invalid = {
  "kind": "books#volumes",
  "totalItems": 197}

class MockRequest:
  def __init__(self, json):
    self.json = json

request_valid = MockRequest({
        "acquired": 'true',
        "authors": [
            "Karolina Jarosz"
        ],
        "external_id": 'null',
        "published_year": "2000",
        "thumbnail": 'null',
        "title": "Python is great!"
    })

request_invalid = 'invalid'

class MockBookObject:
  def __init__(self, _id, external_id, title, authors, acquired, published_year, thumbnail):
    self._id = _id
    self.external_id = external_id
    self.title = title
    self.authors = authors
    self.acquired = acquired
    self.published_year = published_year
    self.thumbnail = thumbnail

book_valid = MockBookObject(1, '123', 'Python is great!', 'Karolina Jarosz', True, '2020', None)

book_invalid = 'invalid'

filters_valid = {
  "acquired": 'true',
  "authors": "Karolina",
  "from": "2000",
  'to': '2020',
  "title": "Python"
}

filters_invalid = {'store': 'invalid'}