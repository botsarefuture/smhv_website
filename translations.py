# TRANSLATIONS API
class translations():
    def __init__(self, language, config_path="translations.json"):
        self.config_path = config_path
        self.load_config() # Load config
        
        language = language.upper()
        
        if language in self.config.get("languages", []):
            self.language = language
            
        else:
            raise Exception("Invalid language, valid languages are: %s" % self.config.get("languages", []))
        
        
    
    def load_config(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)
            self.config = config
    
    def get_translations(self, page=None):
        translations = self.config
        
        urtranslations = translations.get(self.language) # Translation in your language
        
        
        if page == None:
            return urtranslations
        
        pagetranslations = urtranslations.get(page)
        
        return pagetranslations
    
    def get_translation(self, page, slug):
        translations = self.config
        
        urtranslations = translations.get(self.language)
        
        pagetranslations = urtranslations.get(page)
        
        slugtranslation = pagetranslations.get(slug)
        
        print(slugtranslation)
        
        return slugtranslation
        
        
    
    def set_language(self, language):
        self.language = language


