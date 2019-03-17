class SingleChoice < ApplicationRecord
  validates :touch_id, presence: true
  validates :single_answer_id, presence: true
end
