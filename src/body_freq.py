import pandas as pd
import numpy as np
import spacy
import seaborn as sns
sns.set_theme(style="whitegrid", context="talk")
import matplotlib.pyplot as plt
from adjustText import adjust_text

#load data
df = pd.read_csv("/Users/thearolskovsloth/data-science-x-am/output/body_descriptions.csv")

#lowercase all body parts
df["bodypart"] = df["bodypart"].str.lower()

#lemmatize all the bodyparts
nlp = spacy.load("en_core_web_sm")
nlp.disable_pipes("ner", "parser")
nlp.max_length = 2568609
lemmas = df.bodypart.str.cat(sep=' ')
lemmatized_bodyparts = nlp(lemmas)

#apply to all bodypart obs
lemmatized_body = [w.lemma_ for w in lemmatized_bodyparts]

#overwrite the bodypart column with the lemmatied bodyparts
df['bodypart'] = lemmatized_body

#manual lemmatize "lips"
df['bodypart'] = np.where(df['bodypart'] == "lips", "lip", df['bodypart'])
df.loc[df['bodypart'] == "lips"]

#set the top x words to investigate
top = 50

#select male authors
m_authors = df.loc[(df['author_gender']=="M")]
m_authors_total_bodycount = m_authors['bodypart'].value_counts().sum()

#select the top x bodypart mentions from the bodyparts column
top_m_authors = m_authors['bodypart'].value_counts()[:top].rename_axis('bodypart').reset_index(name='top_m_authors')

#to a list
top_m_authors_list = list(top_m_authors['bodypart'])

#the standardized measure for female authors: # of mentions of bodypart x / sum of all bodypart mentions for male owners
top_m_authors['std_male_authors'] = top_m_authors.apply (lambda row: (row.top_m_authors)/m_authors_total_bodycount, axis=1)

#select female authors
f_authors = df.loc[(df['author_gender']=="F")]

f_authors_total_bodycount = f_authors['bodypart'].value_counts().sum()

#select the top x bodypart mentions from the bodyparts column
top_f_authors = f_authors['bodypart'].value_counts()[:top].rename_axis('bodypart').reset_index(name='top_f_authors')

#to list for later use
top_f_authors_list = list(top_f_authors['bodypart'])

#the standardized measure for female authors: # of mentions of bodypart x / sum of all bodypart mentions for male owners
top_f_authors['std_female_authors'] = top_f_authors.apply (lambda row: (row.top_f_authors)/f_authors_total_bodycount, axis=1)

sns.barplot(x = 'std_female_authors',
            y = 'bodypart',
            data = top_f_authors,
            palette = "flare").set(title=f'Top {top} bodyparts mentioned by female authors',xlabel = "Probability of bodypart", ylabel = "Bodypart")
 
#save the plot
plt.savefig('females.png')

males_interesting = sns.barplot(x = 'std_male_authors',
            y = 'bodypart',
            data = top_m_authors,
            palette = "crest").set(title=f'Top {top} bodyparts mentioned by male authors',xlabel = "Probability of bodypart", ylabel = "Bodypart")

#save the plot
plt.savefig('males.png')

#defined list of 30 body words to investigate further
interesting_bodyparts = ['eye', 'hand', 'face', 'arm', 'mouth', 'breast', 'heart', 'shoulder', 'lip', 'body', 'hair', 'neck', 'head', 'back', 'brain', 'nose', 'tooth', 'fist', 'tongue', 'chin', 'chest', 'forehead', 'skin', 'lap', 'waist', 'jaw', 'stomach', 'pupil', 'eyebrow', 'ankle']


#ANALYSIS OF OWNER GENDER

#FEMALE AUTHORS - 2 dataframes, 1 for each owner gender
#male owners
male_owners_female_authors = df.loc[(df['owner_gender']=="M") & (df['author_gender']=="F")]
#female owners
female_owners_female_authors = df.loc[(df['owner_gender']=="F") & (df['author_gender']=="F")]

#MALE AUTHORS - 2 dataframes, 1 for each owner gender
#male owners
male_owners_male_authors = df.loc[(df['owner_gender']=="M") & (df['author_gender']=="M")]
#female owners
female_owners_male_authors = df.loc[(df['owner_gender']=="F") & (df['author_gender']=="M")]

#FEMALE AUTHORS - freq body parts
#male_owners
male_owners_female_authors_counts = male_owners_female_authors['bodypart'].value_counts().rename_axis('bodypart').reset_index(name='counts_male_owners_female_authors')
#female_owners
female_owners_female_authors_counts = female_owners_female_authors['bodypart'].value_counts().rename_axis('bodypart').reset_index(name='counts_female_owners_female_authors')
#get totalt number of body mentions - female authors, male owners
total_male_owners_female_authors_count = male_owners_female_authors_counts['counts_male_owners_female_authors'].sum()
#get totalt number of body mentions - female authors, female owners
total_female_owners_female_authors_count = female_owners_female_authors_counts['counts_female_owners_female_authors'].sum()
print("total_male_owners_female_authors_count:", total_male_owners_female_authors_count, "total_female_owners_female_authors_count:",total_female_owners_female_authors_count)

#keep only the bodyparts that are in the top x female words list
#male owners
male_owners_female_authors_counts = male_owners_female_authors_counts[male_owners_female_authors_counts['bodypart'].isin(interesting_bodyparts)]
#female owners
female_owners_female_authors_counts = female_owners_female_authors_counts[female_owners_female_authors_counts['bodypart'].isin(interesting_bodyparts)]

#MALE AUTHORS - freq body parts

#male_owners
male_owners_male_authors_counts = male_owners_male_authors['bodypart'].value_counts().rename_axis('bodypart').reset_index(name='counts_male_owners_male_authors')
#female_owners
female_owners_male_authors_counts = female_owners_male_authors['bodypart'].value_counts().rename_axis('bodypart').reset_index(name='counts_female_owners_male_authors')
#get totalt number of body mentions - female authors, male owners
total_male_owners_male_authors_count = male_owners_male_authors_counts['counts_male_owners_male_authors'].sum()
#get totalt number of body mentions - female authors, female owners
total_female_owners_male_authors_count = female_owners_male_authors_counts['counts_female_owners_male_authors'].sum()
print("total_male_owners_male_authors_count:", total_male_owners_male_authors_count, "total_female_owners_male_authors_count:",total_female_owners_male_authors_count)

#keep only the bodyparts that are in the top x male words list
#male_owners
male_owners_male_authors_counts = male_owners_male_authors_counts[male_owners_male_authors_counts['bodypart'].isin(interesting_bodyparts)]
#female_owners
female_owners_male_authors_counts = female_owners_male_authors_counts[female_owners_male_authors_counts['bodypart'].isin(interesting_bodyparts)]

#standardize measures

#FEMALE AUTHORS

#the standardized measure for male owners: # of mentions of bodypart x / sum of all bodypart mentions for male owners
male_owners_female_authors_counts['std_male_owners_female_authors'] = male_owners_female_authors_counts.apply (lambda row: (row.counts_male_owners_female_authors)/total_male_owners_female_authors_count, axis=1)

#the standardized measure for female owners: # of mentions of bodypart x / sum of all bodypart mentions for female owners
female_owners_female_authors_counts['std_female_owners_female_authors'] = female_owners_female_authors_counts.apply (lambda row: (row.counts_female_owners_female_authors)/total_female_owners_female_authors_count, axis=1)

#MALE AUTHORS

#the standardized measure for male owners: # of mentions of bodypart x / sum of all bodypart mentions for male owners
male_owners_male_authors_counts['std_male_owners_male_authors'] = male_owners_male_authors_counts.apply (lambda row: (row.counts_male_owners_male_authors)/total_male_owners_male_authors_count, axis=1)

#the standardized measure for female owners: # of mentions of bodypart x / sum of all bodypart mentions for female owners
female_owners_male_authors_counts['std_female_owners_male_authors'] = female_owners_male_authors_counts.apply (lambda row: (row.counts_female_owners_male_authors)/total_female_owners_male_authors_count, axis=1)

#merge into author gender data frames

female_authors = pd.merge(male_owners_female_authors_counts, female_owners_female_authors_counts, on=['bodypart'])
male_authors = pd.merge(male_owners_male_authors_counts, female_owners_male_authors_counts, on=['bodypart'])

#sort alphabetically

male_authors= male_authors.sort_values(by = "bodypart", axis=0, ascending=True)
female_authors= female_authors.sort_values(by = "bodypart", axis=0, ascending=True)

#calculate skew

#male authors
male_authors['skewness_male_authors'] = np.where(male_authors['std_male_owners_male_authors'] > male_authors['std_female_owners_male_authors'], ((male_authors['std_male_owners_male_authors'])/(male_authors['std_female_owners_male_authors'])), ((-male_authors['std_female_owners_male_authors'])/male_authors['std_male_owners_male_authors']))
male_authors['n'] = range(len(male_authors))
male_authors['skew_direction'] = np.where(male_authors['skewness_male_authors'] > 0, "male_skew", "female_skew")
#subtract 1
male_authors['skewness_male_authors'] = np.where(male_authors['skewness_male_authors'] > 0, male_authors['skewness_male_authors']-1,male_authors['skewness_male_authors']+1)

#female authors
female_authors['skewness_female_authors'] = np.where(female_authors['std_male_owners_female_authors'] > female_authors['std_female_owners_female_authors'], ((female_authors['std_male_owners_female_authors'])/(female_authors['std_female_owners_female_authors'])), ((-female_authors['std_female_owners_female_authors'])/female_authors['std_male_owners_female_authors']))
female_authors['n'] = range(len(female_authors))
female_authors['skew_direction'] = np.where(female_authors['skewness_female_authors'] > 0, "male_skew", "female_skew")
#subtract 1
female_authors['skewness_female_authors'] = np.where(female_authors['skewness_female_authors'] > 0, female_authors['skewness_female_authors']-1,female_authors['skewness_female_authors']+1)

#visualize

#join x values
x = list(male_authors['skewness_male_authors'])+list(female_authors['skewness_female_authors'])

sns.set_style("whitegrid")
x = list(male_authors['skewness_male_authors'])+list(female_authors['skewness_female_authors'])
y = list(range(0,30))+list(range(0,30))
fig = plt.figure()
ax1 = fig.add_subplot(111)
#fig, ax = plt.subplots()

ax1.scatter(x[:30], y[:30], s=20, c='seagreen', marker="s", label='male authors', alpha = 0.7)
ax1.scatter(x[30:],y[30:], s=20, c='coral', marker="o", label='female authors', alpha = 0.7)

texts = []
for i, txt in enumerate(male_authors.bodypart):
    texts.append(ax1.annotate(txt, (male_authors.skewness_male_authors.iat[i],male_authors.n.iat[i]), color = "seagreen"))
for i, txt in enumerate(female_authors.bodypart):
    texts.append(ax1.annotate(txt, (female_authors.skewness_female_authors.iat[i],female_authors.n.iat[i]), color = "coral"))
    
adjust_text(texts)

frame1 = plt.gca()
frame1.axes.yaxis.set_ticklabels([])
frame1.axes.xaxis.set_ticks([-41, -36, -11, -6, -2, -1, 0, 1, 2, 6, 11])
frame1.axes.xaxis.set_ticklabels(ticklabels =['40 x','35 x','10 x', '5 x', '3 x', '2 x', '50/50', '2 x', '3 x', '5 x', '10 x'], rotation=65, size=12)

plt.axvline(0, ls = "--", color="grey")

plt.legend(loc='lower left');
plt.title('Male and female body parts, by author gender')
plt.xlabel('female                                                                Skewness                                                                  male')
ax1.yaxis.set_visible(False)
plt.xlim(-7,7)
fig.set_figheight(15)
fig.set_figwidth(10)
plt.savefig('skewness1.png')










